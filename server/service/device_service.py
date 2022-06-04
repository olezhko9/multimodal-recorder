from bson import ObjectId

from model.device import Device


def get_devices():
    devices = Device.objects()
    return [device.to_mongo() for device in devices]


def delete_device(subject_id):
    device = Device.objects(_id=ObjectId(subject_id)).first()
    if device:
        device.delete()
