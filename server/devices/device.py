from abc import ABC, abstractmethod
import threading


class Device(ABC, threading.Thread):
    def __init__(self, options):
        threading.Thread.__init__(self)
        self.options = options
        self.started = False
        self._stop_event = threading.Event()

    @abstractmethod
    def start(self):
        self.started = True
        threading.Thread.start(self)

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def stop(self):
        self._stop_event.set()
        self.started = False

    @abstractmethod
    def get_data(self):
        if not self.started:
            raise Exception('Device is not started')
