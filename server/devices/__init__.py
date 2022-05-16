import threading

from queue import Queue

from .openbci import OpenBCIBoard
from .camera import Camera


def get_device_class(all_devices, device_id):
    device_config = [device for device in all_devices if device['device_id'] == device_id]
    if len(device_config):
        device_config = device_config[0]
        device_class = globals().get(device_config.get('class'))
        return device_class
    else:
        return None


class DeviceManager(threading.Thread):
    def __init__(self, all_devices):
        threading.Thread.__init__(self)
        self.all_devices = all_devices
        self._devices = {}
        self._isProcessingData = False
        self.stream_queue = Queue()
        self.read_queue = Queue()
        self._streamingDevices = {}

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

    def remove_device(self, device_id):
        self._devices.pop(device_id, None)

    def stop_and_remove_devices(self):
        self._isProcessingData = False

        for device_id in list(self._devices):
            try:
                self.stop_stream(device_id)
                self._devices[device_id].stop_record()
            except Exception:
                pass
            self.remove_device(device_id)

    def get_devices(self):
        return self._devices

    def get_device(self, device_id):
        return self._devices.get(device_id)

    def run(self):
        while True:
            if not self._isProcessingData:
                return

            for device_id in self._devices:
                device = self.get_device(device_id)
                data = device.get_data()

                if data is not None:
                    self.read_queue.put((device_id, data))

                    if self._streamingDevices.get(device_id, None):
                        self.stream_queue.put((device_id, device.format_to_sse(data)))

    def read_data(self):
        self._isProcessingData = True
        if not self.is_alive():
            threading.Thread.start(self)

        return self.read_queue

    def start_stream(self, device_id):
        self._streamingDevices[device_id] = True
        return self.stream_queue

    def stop_stream(self, device_id):
        self._streamingDevices.pop(device_id, None)

    def get_data_stream(self):
        return self.read_queue
