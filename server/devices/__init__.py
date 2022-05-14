import json

from .eeg_board import EEGBoard
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
