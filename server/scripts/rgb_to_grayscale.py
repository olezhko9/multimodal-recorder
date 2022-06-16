from cv2 import cv2


def run(data, options, device):
    for i in range(len(data)):
        data[i] = cv2.cvtColor(data[i], cv2.COLOR_BGR2GRAY)

    return data


def get_config():
    return {
        'modalities': ['visual/image'],
        'doc': 'Конвертировать RGB изображение в черно-белое',
        'arguments': {}
    }
