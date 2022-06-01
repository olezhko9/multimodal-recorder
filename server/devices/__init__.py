from .openbci import OpenBCIBoard
from .camera import Camera
from .arduino import ArduinoUNO
from .tobii import Tobii


def get_device_class(all_devices, device_id):
    device_config = [device for device in all_devices if device['device_id'] == device_id]
    if len(device_config):
        device_config = device_config[0]
        device_class = globals().get(device_config.get('class'))
        return device_class
    else:
        return None
