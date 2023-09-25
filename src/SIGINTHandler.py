import logging
import signal

def RegisterSIGINTHandler():
    logging.debug("Registering SIGINT handler")
    handler = SIGINT_handler()
    signal.signal(signal.SIGINT, handler.signal_handler)
    return handler

class SIGINT_handler():

    def __init__(self):
        self.SIGINT = False

    def signal_handler(self, signal, frame):
        logging.debug('You pressed Ctrl+C!')
        self.SIGINT = True
