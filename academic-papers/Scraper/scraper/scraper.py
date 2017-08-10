from functools import partial
from result import Result, track, result_of, error_of
from time import sleep
import oai


class WaitError:

    def __init__(self, wait):
        self.wait = wait

class OutOfSpaceError:

    def __init__(self, attempted, available):
        self.attempted = attempted
        self.available = available


@track('R:R')
def check_wait(result):
    if (result.type == Result.ERROR
            and isinstance(result.get(), oai.HttpStatus)
            and result.get().code == 503):
        msg = result.get().response
        if msg.headers.get('Retry-After', '').isdigit():
            return error_of(WaitError(int(msg.headers['Retry-After'])))
    else:
        return result


@track('VV:R')
def store(data, storage):
    if not storage.has_space(data):
        return \
            error_of(OutOfSpaceError(len(data), storage.available_storage()))
    resumption_token = oai.resumption_token_from_response(data)
    storage.store(data)
    storage.log_resumption(resumption_token)
    return result_of(data)


def send_and_store_single_request(storage, request):
    res = request()
    res = check_wait(res)
    res = res.with_obj(storage)
    res = store(res)
    return res


def send_and_store_many_requests(storage, response_handler, initial,
                                 max_requests = None, suggested_wait = 0):
    assert suggested_wait >= 0
    request = initial
    num_requests = 0
    wait_time = 0
    has_space = True
    while (has_space and
               (max_requests is None
                or num_requests < max_requests)):
        result = send_and_store_single_request(storage, request)
        if result.type == Result.SUCCESS:
            [response_data] = result.get()
            resumption_token = \
                oai.resumption_token_from_response(response_data)
            request = partial(oai.resume_request_list_records,
                              response_handler, resumption_token)
            num_requests += 1
            print(f'Downloaded request no. {num_requests}.')
        elif isinstance(result.get(), WaitError):
            wait_time = result.get().wait
            print(f'Recieved wait with time {wait_time}.')
        elif isinstance(result.get(), OutOfSpaceError):
            print(f'Out of space.')
            has_space = False
        else:
            raise RuntimeError(f'Unexpected error of type '
                               f'{type(result.get()).__name__}')
        sleep_time = max(suggested_wait, wait_time)
        print(f'Sleeping for {sleep_time} seconds.')
        sleep(sleep_time)
