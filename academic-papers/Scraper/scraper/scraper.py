from functools import partial
from time import sleep
import oai


class WaitError(Exception):

    def __init__(self, wait):
        self.wait = wait

class OutOfSpaceError(Exception):

    def __init__(self, attempted, available):
        self.attempted = attempted
        self.available = available


def check_wait(error):
    if (isinstance(error, oai.HttpStatusError) and error.code == 503):
        msg = error.response
        if msg.headers.get('Retry-After', 'not digits').isdigit():
            raise WaitError(int(msg.headers['Retry-After']))


def store(data, storage):
    if not storage.has_space(data):
        raise OutOfSpaceError(len(data), storage.available_storage())
    resumption_token = oai.resumption_token_from_response(data)
    storage.store(data)
    storage.log_resumption(resumption_token)


def send_and_store_single_request(storage, request):
    try:
        data = request()
        store(data, storage)
        return data
    except oai.HttpStatusError as err:
        # see if the http status error should be converted to a wait error
        check_wait(err)
        # otherwise re-raise original error
        raise


def send_and_store_many_requests(storage, response_handler, initial,
                                 max_requests = None, suggested_wait = 0):
    assert suggested_wait >= 0
    request = initial
    num_requests = 0
    wait_time = 0
    has_space = True
    while (has_space
           and (max_requests is None
                or num_requests < max_requests)):
        try:
            data = send_and_store_single_request(storage, request)
            resumption_token = oai.resumption_token_from_response(data)
            request = partial(oai.resume_request_list_records,
                              response_handler, resumption_token)
            num_requests += 1
            print(f'Downloaded request #{num_requests}.')
        except oai.HttpStatusError as err:
            raise RuntimeError(f'Unhandled http response with code '
                               f'{err.code}') from err
        except oai.ApplicationError as err:
            raise RuntimeError(f'Unhandled OAI error of type '
                               f'{err.error}') from err
        except WaitError as err:
            wait_time = err.wait
            print(f'Recieved wait with time {wait_time}.')
        except OutOfSpaceError as err:
            has_space = False
            print(f'Ran out of space.')
        except Exception as err:
            raise RuntimeError(f'Encountered error of unexpected type '
                               f'{type(err).__name__}.')

        sleep_time = max(suggested_wait, wait_time)
        print(f'Sleeping for {sleep_time} seconds.')
        sleep(sleep_time)
