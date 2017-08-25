import pykka


class Monitor(pykka.ThreadingActor):

    def __init__(self):
        pass

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_failure(self, exception_type, exception_value, traceback):
        pass

    def on_receive(self, message):
        pass