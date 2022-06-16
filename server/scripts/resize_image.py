from cv2 import cv2


def run(data, options, device):
    for i in range(len(data)):
        image = data[i]
        width = options.get('width') or image.shape[1]
        height = options.get('height') or image.shape[0]
        data[i] = cv2.resize(data[i], (width, height), interpolation=cv2.INTER_AREA)

    return data


def get_config():
    return {
        'modalities': ['visual/image'],
        'doc': 'Изменить размер изображения',
        'arguments': {
            'width': {
                'doc': 'Новая ширина',
                'type': 'number'
            },
            'height': {
                'doc': 'Новая высота',
                'type': 'number'
            }
        }
    }
