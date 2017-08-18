# Test libraries
import httpretty
import context
import pytest
import requests

# UUT
import oai
import result

#
# Utility functions
# 

def get_error_code(filename):
    e_idx = len('error_')
    x_idx = len('.xml')
    if filename[-x_idx - 1].isdigit():
        stripped = filename[e_idx:(-x_idx - 2)]
    else:
        stripped = filename[e_idx:-x_idx]
    # snake_case -> camelCase
    code = ''
    cap = False # error codes are camelCase
    idx = 0
    while idx < len(stripped):
        if stripped[idx] == '_':
            cap = True
        else:
            if cap:
                code += stripped[idx].upper()
            else:
                code += stripped[idx]
            cap = False
        idx += 1
    return code


def get_success_method(filename):
    s_idx = len('success_response_')
    x_idx = len('.xml')
    if filename[-x_idx - 1].isdigit():
        stripped = filename[s_idx:(-x_idx - 2)]
    else:
        stripped = filename[s_idx:-x_idx]
    # snake_case -> PascalCase
    method = ''
    cap = True  # methods are PascalCase
    idx = 0
    while idx < len(stripped):
        if stripped[idx] == '_':
            cap = True
        else:
            if cap:
                method += stripped[idx].upper()
            else:
                method += stripped[idx]
            cap = False
        idx += 1
    return method


def get_error_xml_filenames():
    import os
    data_path = os.path.join(os.path.dirname(__file__), 'data/')
    paths = os.listdir(data_path)
    return filter(lambda path: 'error' in path, paths)


def get_success_xml_filenames():
    import os
    data_path = os.path.join(os.path.dirname(__file__), 'data/')
    paths = os.listdir(data_path)
    return filter(lambda path: 'success' in path, paths)


def data_file_path(filename):
    import os
    return os.path.join(os.path.dirname(__file__), 'data', filename)


def response_handler(data):
    return requests.post('http://archive.org/oai', data)

#
# Utility function tests
#

def test_get_error_code():
    assert get_error_code('error_some_code.xml') == 'someCode'
    assert get_error_code('error_some_code_1.xml') == 'someCode'

#
# Fixtures
#

@pytest.fixture(scope='module')
def base_url():
    return 'http://archive.org/oai'


@pytest.fixture(scope='module',
                params=[201, 204, 301, 400, 404, 500, 503])
def http_code(request):
    return request.param 


@pytest.fixture(scope='module',
                params=get_error_xml_filenames())
def error_response(request):
    return (request.param, get_error_code(request.param))


@pytest.fixture(scope='module',
                params=get_success_xml_filenames())
def success_response(request):
    return (request.param, get_success_method(request.param))

#
# Unit tests
#

# MAINTENANCE NOTE - Things to test
# Handling bad xml (defaults to Success object D:)
# We're not testing for correctness of server,
# .. but we should test that we are detecting an incorrect server.


@httpretty.activate
def test_base_oai_request_sends_post_to_url(base_url):
    httpretty.register_uri(httpretty.POST, base_url)
    response = oai.base_oai_request(response_handler, oai.Verbs.IDENTIFY)
    assert httpretty.has_request()


@httpretty.activate
def test_base_oai_request_handles_http_error_codes(base_url, http_code):
    httpretty.register_uri(
            httpretty.POST,
            base_url,
            status=http_code)
    with pytest.raises(oai.HttpStatusError) as err_info:
        response = oai.base_oai_request(response_handler, oai.Verbs.IDENTIFY)
    assert err_info.value.code == http_code


@httpretty.activate
def test_base_oai_request_handles_application_errors(base_url, error_response):
    # MAINTENANCE NOTE
    # Right now I don't care if the error response is appropriate with respect to
    # the request. Might need to fix this later if the scraper gets picky.
    (filename, code) = error_response
    with open(data_file_path(filename), 'rb') as f:
        xml_data = f.read()
    httpretty.register_uri(httpretty.POST, base_url, status=200, body=xml_data)
    with pytest.raises(oai.ApplicationError) as err_info:
        response = oai.base_oai_request(response_handler, oai.Verbs.LIST_IDENTIFIERS)
    assert err_info.value.error == code
    # MAINTENANCE NOTE:
    # Testing for correct payload should belong in another test in the long run
    assert err_info.value.data == xml_data


@httpretty.activate
def test_base_oai_request_handles_success(base_url, success_response):
    (filename, method) = success_response
    with open(data_file_path(filename), 'rb') as f:
        xml_data = f.read()
    httpretty.register_uri(httpretty.POST, base_url, status=200, body=xml_data)
    data = oai.base_oai_request(response_handler, oai.Verbs.LIST_IDENTIFIERS)
    # MAINTENANCE NOTE
    # need to test payload, probably elsewhere
    assert data == xml_data


@httpretty.activate
def test_oai_request_list_records_sends_expected_request(base_url):
    with open(data_file_path('success_response_list_records.xml'), 'rb') as f:
        data = f.read()
    httpretty.register_uri(httpretty.POST, base_url, status=200, body=data)
    outer_data = None
    def request_handler(inner_data):
        nonlocal outer_data
        outer_data = inner_data
        return requests.post(base_url, inner_data)
    oai.request_list_records(request_handler)
    assert outer_data['verb'] == 'ListRecords'
    assert set(outer_data.keys()) <= {'from', 'until', 'set', 'verb', 'metadataPrefix'}


@httpretty.activate
def test_oai_resume_list_records_sends_expected_request(base_url):
    with open(data_file_path('success_response_list_records.xml'), 'rb') as f:
        data = f.read()
    httpretty.register_uri(httpretty.POST, base_url, status=200, body=data)
    outer_data = None
    def request_handler(inner_data):
        nonlocal outer_data
        outer_data = inner_data
        return requests.post(base_url, inner_data)
    oai.resume_request_list_records(request_handler, 'TOKEN')
    assert outer_data['verb'] == 'ListRecords'
    assert outer_data['resumptionToken'] == 'TOKEN'
    assert set(outer_data.keys()) == {'verb', 'resumptionToken'}

# TODO: test requests have required parameters
