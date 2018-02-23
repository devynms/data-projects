import gevent
import zmq.green as zmq

def create_server(port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f'127.0.0.1:{port}')
    return socket

def serve_request(monitor, server):
    def _serve_request():
        request = server.recv_json()
        monitor.tell({'msg': 'serve',
                      'request': request,
                      'server': server})
    gevent.spawn(_serve_request)
