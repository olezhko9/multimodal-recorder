from abc import ABC, abstractmethod
import multiprocessing as mp


class Device(ABC, mp.Process):
    def __init__(self, options):
        super(Device, self).__init__()
        self.options = options
        self.is_stopped = mp.Event()
        self.buffer = mp.Queue()

    @abstractmethod
    def start(self):
        self.daemon = True
        super(Device, self).start()

    @abstractmethod
    def stop(self):
        self.is_stopped.set()
        self.buffer.cancel_join_thread()
        super(Device, self).terminate()
        super(Device, self).join()

    def is_started(self):
        return not self.is_stopped.is_set()

    def get_data(self):
        if self.buffer.empty():
            return None, False

        return self.buffer.get()
