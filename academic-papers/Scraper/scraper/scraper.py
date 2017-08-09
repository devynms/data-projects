import oai
from time import sleep


def process_single_request(storage, request):
    # MAINTENANCE NOTE
    # want a proper system for handling different possible errors
    # something better than raising (possibly redundant) RuntimeError's
    result = request()
    if isinstance(result, oai.HttpStatus):
        raise RuntimeError(result)
    elif isinstance(result, oai.ApplicationError):
        raise RuntimeError(result)
    # isinstance(response, oai.Success)
    data = result.data
    if not storage.has_space(data):
        raise RuntimeError('out of space')
    storage.store(data)
    token = oai.resumption_token_from_response(data)
    return token


def initial_requestor(response_handler, metadata_prefix='oai_dc',
                      time_from=None, time_until=None, select_set=None):
    def _initial_requestor():
        return oai.request_list_records(response_handler, metadata_prefix,
                                        time_from, time_until, select_set)
    return _initial_requestor


def continue_requestor(response_handler, resumption_token):
    def _continue_requestor():
        return oai.resume_request_list_records(response_handler,
                                               resumption_token)
    return _continue_requestor


def process_many_requests_with_initial(storage, response_handler, initial,
                                       max_requests):
    print(f'beginning (max: ${max_requests}) ...')
    token = process_single_request(storage, initial)
    print(f'completed request, returning token: {token}')
    print('sleeping...')
    sleep(20)
    requests = 1
    while max_requests is None or requests <= max_requests:
        token = process_single_request(
            storage, continue_requestor(response_handler, token))
        print(f'completed request, returning token: {token}')
        requests += 1
        print('sleeping...')
        sleep(20)
