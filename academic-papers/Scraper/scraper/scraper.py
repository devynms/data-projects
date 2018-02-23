from functools import partial
from time import sleep
from scraper import oai


class WaitError(Exception):

    def __init__(self, wait):
        self.wait = wait

class OutOfSpaceError(Exception):

    def __init__(self, attempted, available):
        self.attempted = attempted
        self.available = available


def _is_http_wait(error):
    if isinstance(error, oai.HttpStatusError) \
           and error.code == 503:
        msg = error.response
        return msg.headers.get('Retry-After', 'not digits').isdigit()


def _convert_to_wait_error(error):
    msg = error.response
    return WaitError(int(msg.headers['Retry-After']))


class Worker:

    def __init__(self, storage, response_handler):
        self.storage = storage
        self.response_handler = response_handler

    def _can_continue(self, have_space, num_requests, max_requests):
        return (have_space
                and (max_requests is None
                     or num_requests < max_requests))

    def run(self, initial, max_requests = None, suggested_wait = 0):
        assert suggested_wait >= 0
        assert max_requests is None or max_requests >= 1
        request = self.initial
        num_requests = 0
        wait_time = 0
        has_space = True
        while self.can_continue(has_space, num_requests, max_requests):
            try:
                data = self.store_single_request(request)
                resumption_token = oai.resumption_token_from_response(data)
                request = partial(oai.resume_request_list_records,
                                  self.response_handler, resumption_token)
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

            sleep_time = max(self.suggested_wait, wait_time)
            print(f'Sleeping for {sleep_time} seconds.')
            sleep(sleep_time)

    def store_single_request(self, request):
        try:
            data = request()
            self.store(data)
            return data
        except oai.HttpStatusError as err:
            if _is_http_wait(err):
                raise _convert_to_wait_error(err)
            else:
                raise

    def _store(self, data):
        if not self.storage.has_space(data):
            raise OutOfSpaceError(len(data),
                                  self.storage.available_storage())
        resumption_token = oai.resumption_token_from_response(data)
        self.storage.store(data)
        self.storage.log_resumption(resumption_token)

