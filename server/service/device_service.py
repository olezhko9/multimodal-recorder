from model.device import Device


def get_devices():
    devices = Device.objects()
    return [device.to_mongo() for device in devices]
