import pytest
from scraper import oai
from scraper import storage
from scraper import scraper


@pytest.fixture(scope='module')
def response_handler():
    def _response_handler():
        pass
    return _response_handler


class MockHttpResponse:

    def __init__(self, headers):
        # mock out response fields as needed when tests fail
        self.headers = headers


def test_check_wait_throws_on_503_with_seconds():
    response = MockHttpResponse({'Retry-After': '30'})
    err = oai.HttpStatusError(503, response)
    with pytest.raises(scraper.WaitError) as exc:
        scraper.check_wait(err)
    assert exc.value.wait == 30


def test_check_wait_no_throw_on_503_unknown_time():
    response = MockHttpResponse({'Retry-After': 'a timestamp or something'})
    err = oai.HttpStatusError(503, response)
    try:
        scraper.check_wait(err)
    except scraper.WaitError:
        pytest.fail('Should not throw wait error when timestamp cannot be '
                    'parsed as digits.')

def test_check_wait_no_throw_on_not_503():
    response = None
    err = oai.HttpStatusError(404, response)
    try:
        scraper.check_wait(err)
    except scraper.WaitError:
        pytest.fail('Should not throw wait error when http response code is '
                    'not 503.')

def test_store_throws_on_out_of_space():
    stg = storage.MockStorage(0)
    with pytest.raises(scraper.OutOfSpaceError) as exc:
        scraper.store(b'some data', stg)
    assert stg.store_count == 0
    assert stg.log_resumption_count == 0

def test_store_stores_once_with_available_space():
    stg = storage.MockStorage(100)
    data = b'some data'
    scraper.store(data, stg)
    assert stg.store_count == 1
    assert stg.log_resumption_count == 1

# send_and_store_single_request = 3sr

def test_3sr_stores_good_request_once():
    request = lambda: b'some data'
    stg = storage.MockStorage(100)
    worker = scraper.Worker(stg, request)
    scraper.send_and_store_single_request(stg, request)
    assert stg.store_count == 1
    assert stg.log_resumption_count == 1

def test_3sr_throws_out_of_space():
    request = lambda: b'some data'
    stg = storage.MockStorage(0)
    with pytest.raises(scraper.OutOfSpaceError) as exc:
        scraper.send_and_store_single_request(stg, request)

def test_3sr_throws_wait_error():
    response = MockHttpResponse({'Retry-After': '30'})
    err = oai.HttpStatusError(503, response)
    def request():
        raise err
    stg = storage.MockStorage(100)
    with pytest.raises(scraper.WaitError) as exc:
        scraper.send_and_store_single_request(stg, request)

def test_3sr_passes_http_status_error():
    stg = storage.MockStorage(100)
    def request():
        raise oai.HttpStatusError(404, 'stuff')
    with pytest.raises(oai.HttpStatusError) as exc:
        scraper.send_and_store_single_request(stg, request)
    assert stg.store_count == 0

def test_3sr_passes_application_error():
    stg = storage.MockStorage(100)
    def request():
        raise oai.ApplicationError(oai.ApplicationError.BAD_ARGUMENT,
                                   'text', 'text')
    with pytest.raises(oai.ApplicationError) as exc:
        scraper.send_and_store_single_request(stg, request)
    assert stg.store_count == 0
