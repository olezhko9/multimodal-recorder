import threading

from queue import Queue
from devices import get_device_class


class DeviceManager(threading.Thread):
    def __init__(self, all_devices):
        threading.Thread.__init__(self)
        self.all_devices = all_devices
        self._devices = {}
        self._isProcessingData = False
        self.stream_queue = Queue()
        self.read_queue = Queue()
        self._streamingDevices = {}
        self._isStartedOnce = False

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
        self._devices[device_id].start_record()

    def stop_device(self, device_id):
        try:
            self.stop_stream(device_id)
            self._devices[device_id].stop_record()
        except Exception:
            pass

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
                            self.read_queue.put((device_id, data))

                        if self._streamingDevices.get(device_id, None):
                            self.stream_queue.put((device_id, device.format_to_sse(data)))
                except Exception:  # probably device not started
                    pass

    def read_data(self):
        if not self._isStartedOnce:
            self.start()
            self._isStartedOnce = True

        if not self._isProcessingData:
            self._isProcessingData = True

        return self.read_queue

    def start_stream(self, device_id):
        self._streamingDevices[device_id] = True
        return self.stream_queue

    def stop_stream(self, device_id):
        self._streamingDevices.pop(device_id, None)

    def get_data_stream(self):
        return self.read_queue
