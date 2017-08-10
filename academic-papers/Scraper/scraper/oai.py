"""Scraper OAI module.
Contains functionality for handling single request/response communications
with an OAI server.
OAI version 2.
"""

from bs4 import BeautifulSoup
from result import result_of, error_of


class Verbs:

    GET_RECORD = 'GetRecord'
    IDENTIFY = 'Identify'
    LIST_IDENTIFIERS = 'ListIdentifiers'
    LIST_METADATA_FORMATS = 'ListMetadataFormats'
    LIST_RECORDS = 'ListRecords'
    LIST_SETS = 'ListSets'

    ALL_VERBS = {
        GET_RECORD, IDENTIFY, LIST_IDENTIFIERS, LIST_METADATA_FORMATS,
        LIST_RECORDS, LIST_SETS
    }


class HttpStatus:

    def __init__(self, code, response):
        self.code = code
        self.response = response

    def __str__(self):
        return f'HttpStatus[code={self.code},data={self.response}]'


class ApplicationError:

    BAD_ARGUMENT = 'badArgument'
    BAD_RESUMPTION_TOKEN = 'badResumptionToken'
    BAD_VERB = 'badVerb'
    CANNOT_DISSEMINATE_FORMAT = 'cannotDisseminateFormat'
    ID_DOES_NOT_EXIST = 'idDoesNotExist'
    NO_RECORDS_MATCH = 'noRecordsMatch'
    NO_METADATA_FORMATS = 'noMetadataFormats'
    NO_SET_HIERARCHY = 'noSetHierarchy'

    VALID_ERRORS = {
        BAD_ARGUMENT,
        BAD_RESUMPTION_TOKEN,
        BAD_VERB,
        CANNOT_DISSEMINATE_FORMAT,
        ID_DOES_NOT_EXIST,
        NO_RECORDS_MATCH,
        NO_METADATA_FORMATS,
        NO_SET_HIERARCHY
    }

    APPLICABLE_VERBS = {
            BAD_ARGUMENT: Verbs.ALL_VERBS,
            BAD_RESUMPTION_TOKEN: {
                Verbs.LIST_IDENTIFIERS,
                Verbs.LIST_RECORDS,
                Verbs.LIST_SETS
            },
            BAD_VERB: set(),
            CANNOT_DISSEMINATE_FORMAT: {
                Verbs.GET_RECORD,
                Verbs.LIST_IDENTIFIERS,
                Verbs.LIST_RECORDS
            },
            ID_DOES_NOT_EXIST: {
                Verbs.GET_RECORD,
                Verbs.LIST_METADATA_FORMATS
            },
            NO_RECORDS_MATCH: {
                Verbs.LIST_IDENTIFIERS,
                Verbs.LIST_RECORDS
            },
            NO_METADATA_FORMATS: {
                Verbs.LIST_METADATA_FORMATS
            },
            NO_SET_HIERARCHY: {
                Verbs.LIST_SETS,
                Verbs.LIST_IDENTIFIERS,
                Verbs.LIST_RECORDS
            }
        }

    def __init__(self, error, error_text, data):
        if error not in ApplicationError.VALID_ERRORS:
            raise ValueError(f'{error} is not a valid application error.')
        self.error = error
        self.error_text = error_text
        self.data = data

    def __str__(self):
        return f'ApplicationError[{self.error}, {self.error_text}]'


def base_oai_request(response_handler, verb, arguments={}):
    """ Sends a raw OAI-PMH request, and returns the response.
    Return:
        | Success:
            | Data (raw xml)
        + HttpStatus
            | 302 Redirect
            + 503 Unavailable
                | Retry-After
        + ApplicationError:
            | badArgument
            + badResumptionToken
            + cannotDisseminateFormat
            + noRecordsMatch
            + noSetHierarchy
            + unexpected
    """
    data = arguments.copy()
    data['verb'] = verb
    response = response_handler(data)
    if response.status_code != 200:
        return error_of(HttpStatus(response.status_code, response))
    else:
        response.encoding = 'utf-8'
        xml_text = response.text
        xml_soup = BeautifulSoup(xml_text, 'lxml-xml')
        if xml_soup.error is not None:
            error = xml_soup.error['code']
            error_text = xml_soup.error.get_text()
            return \
                error_of(ApplicationError(error, error_text, response.content))
        else:
            return result_of(response.content)


def request_list_records(response_handler, metadata_prefix='oai_dc',
                         time_from=None, time_until=None, select_set=None):
    """Calls the ListRecords method, with an initial set of parameters.
    Return: see base_oai_request
    """
    arguments = {}
    arguments['metadataPrefix'] = metadata_prefix
    if time_from:
        arguments['from'] = time_from
    if time_until:
        arguments['until'] = time_until
    if select_set:
        arguments['set'] = select_set
    return base_oai_request(
        response_handler=response_handler,
        verb='ListRecords',
        arguments=arguments
    )


def resume_request_list_records(response_handler, resumption_token):
    """Call the ListIdentifiers method, using a resumption token.
    Return: see base_oai_request
    """
    return base_oai_request(
        response_handler=response_handler,
        verb='ListRecords',
        arguments={
            'resumptionToken': resumption_token
        }
    )


def resumption_token_from_response(response_data):
    """Might raise, for now"""
    xml_data = BeautifulSoup(response_data, 'lxml-xml')
    resumption_token = xml_data.resumptionToken
    if not resumption_token:
        return None
    return resumption_token.text
