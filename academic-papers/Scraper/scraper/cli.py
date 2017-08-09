import argparse
import scraper
import requests
import storage

def handler(url):
    def _handler(data):
        return requests.post(url, data)
    return _handler

def _main(args):
    print(args)
    token = args.token
    max_times = args.max
    my_handler = handler(args.source)
    my_storage = storage.LocalStorage(args.directory)
    scraper.process_many_requests_with_initial(my_storage, my_handler, scraper.initial_requestor(my_handler), max_times)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper (worker)')
    parser.add_argument('-s', '--source', help='base url of source', required=True)
    parser.add_argument('-t', '--token', help='token to start with')
    parser.add_argument('-d', '--directory', help='output directory', required=True)
    parser.add_argument('-m', '--max', help='maximum number of requests to process', type=int)
    args = parser.parse_args()
    _main(args)

