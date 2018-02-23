import pykka.gevent
from scraper import listener


class Monitor(pykka.gevent.GeventActor):

    def __init__(self):
        pass

    def on_start(self):
        server = listener.create_server(8080)
        listener.serve_request(self, server)

    def on_stop(self):
        pass

    def on_failure(self, exception_type, exception_value, traceback):
        pass

    def on_receive(self, message):
        if message['msg'] == 'serve':
            request = message['request']
            server = message['server']
            response = { 'request': request, 'response': 'data' }
            server.send(str(response))
            listener.serve_request(self, server)
        elif message['msg'] == 'update':
            pass
