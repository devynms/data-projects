import argparse
import requests
from functools import partial
from scraper import storage
from scraper import oai
from scraper import scraper


def handler(url):
    def _handler(data):
        return requests.post(url, data)
    return _handler


def _main(args):
    print(args)
    token = args.token
    max_times = args.max
    suggested_wait = args.wait_time
    my_handler = handler(args.source)
    my_storage = storage.LocalStorage(args.directory)
    scraper.send_and_store_many_requests(
        my_storage, my_handler, partial(oai.request_list_records, my_handler),
        max_times, suggested_wait
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper (worker)')
    parser.add_argument('-s', '--source',
                        help='base url of source', required=True)
    parser.add_argument('-w', '--wait-time',
                        help='suggested wait time', type=int, default=0)
    parser.add_argument('-t', '--token',
                        help='token to start with')
    parser.add_argument('-d', '--directory',
                        help='output directory', required=True)
    parser.add_argument('-m', '--max',
                        help='maximum number of requests to process', type=int)
    args = parser.parse_args()
    _main(args)
