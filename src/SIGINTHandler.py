import logging

class SIGINT_handler():

    def __init__(self):
        self.SIGINT = False

    def signal_handler(self, signal, frame):
        logging.debug('You pressed Ctrl+C!')
        self.SIGINT = True
