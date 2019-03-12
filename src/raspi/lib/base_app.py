
import threading, time, signal

from datetime import timedelta

WAIT_TIME_SECONDS = 1

class ProgramKilled(Exception):
    pass

def signal_handler(signum, frame):
    raise ProgramKilled

class App(object):
    def __init__(self, name, loop, *args, **kwargs):
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        self.name = name
        self.loop = loop
        self.args = args
        self.kwargs = kwargs
        self.stopped = False

    def run(self):
        try:
            while not self.stopped:
                self.loop(self.args, self.kwargs)
        except ProgramKilled:
            self.stopped = True
