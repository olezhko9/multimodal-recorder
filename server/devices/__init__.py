import json
import threading

from .openbci import OpenBCIBoard
from .camera import Camera

all_devices = []
with open("./devices.json") as devices_json:
    all_devices = json.load(devices_json)


def get_device_class(device_id):
    device_config = [device for device in all_devices if device['id'] == device_id]
    if len(device_config):
        device_config = device_config[0]
        device_class = globals().get(device_config.get('class'))
        return device_class
    else:
        return None


class DeviceManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._devices = {}

    def add_device(self, device_id, device_options=None):
        if device_options is None:
            device_options = {}

        if self.get_device(device_id) is not None:
            raise Exception(f"Device with id [{device_id}] already exists")

        DeviceClass = get_device_class(device_id)
        if DeviceClass is None:
            raise Exception(f"Device class for device_id [{device_id}] not found")

        self._devices[device_id] = DeviceClass(device_options)

    def add_and_run_device(self, device_id, device_options):
        self.add_device(device_id, device_options)
        self._devices[device_id].start_record()

    def remove_device(self, device_id):
        self._devices.pop(device_id, None)

    def stop_and_remove_devices(self):
        for device_id in list(self._devices):
            try:
                self._devices[device_id].stop_record()
            except Exception:
                pass
            self.remove_device(device_id)

    def get_devices(self):
        return self._devices

    def get_device(self, device_id):
        return self._devices.get(device_id)
