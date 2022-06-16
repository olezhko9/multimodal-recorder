import threading
import traceback

from queue import Queue
from devices import get_device_class


class DeviceManager(threading.Thread):
    def __init__(self, all_devices):
        threading.Thread.__init__(self)
        self.all_devices = all_devices
        self._isStartedOnce = False
        self._isProcessingData = False
        self._devices = {}
        self._stream_queues = {}
        self._read_queue = Queue()

    def add_device(self, device_id, device_options=None):
        if device_options is None:
            device_options = {}

        if self.get_device(device_id) is not None:
            raise Exception(f"Device with id [{device_id}] already exists")

        DeviceClass = get_device_class(self.all_devices, device_id)
        if DeviceClass is None:
            raise Exception(f"Device class for device_id [{device_id}] not found")

        self._devices[device_id] = DeviceClass(device_options)

    def add_and_run_device(self, device_id, device_options):
        self.add_device(device_id, device_options)
        self._devices[device_id].start()

    def stop_device(self, device_id):
        try:
            self.stop_stream(device_id)
            self._devices[device_id].stop()
        except Exception:
            traceback.print_exc()

    def remove_device(self, device_id):
        self._devices.pop(device_id, None)

    def stop_and_remove_device(self, device_id):
        if len(self._devices.keys()) == 1:
            self._isProcessingData = False

        self.stop_device(device_id)
        self.remove_device(device_id)

    def stop_and_remove_devices(self):
        self._isProcessingData = False

        for device_id in list(self._devices):
            self.stop_device(device_id)
            self.remove_device(device_id)

    def get_devices(self):
        return self._devices

    def get_device(self, device_id):
        return self._devices.get(device_id, None)

    def run(self):
        while True:
            if not self._isProcessingData:
                continue

            for device_id in list(self._devices):
                device = self.get_device(device_id)
                try:
                    data, should_save = device.get_data()
                    if data is not None:
                        if should_save:
                            self._read_queue.put((device_id, data))

                        if self._stream_queues.get(device_id, None):
                            self._stream_queues[device_id].put(device.format_to_sse(data))
                except Exception:  # probably device not started
                    traceback.print_exc()

    def read_data(self):
        if not self._isStartedOnce:
            self.start()
            self._isStartedOnce = True

        if not self._isProcessingData:
            self._isProcessingData = True

        return self._read_queue

    def start_stream(self, device_id):
        self._stream_queues[device_id] = Queue()
        return self._stream_queues

    def stop_stream(self, device_id):
        self._stream_queues.pop(device_id, None)

    def get_device_stream(self, device_id):
        return self._stream_queues.get(device_id)

    def get_data_stream(self):
        return self._read_queue
