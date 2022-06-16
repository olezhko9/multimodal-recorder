import numpy as np
from sklearn.preprocessing import MinMaxScaler


def run(data, options, device):
    data_copy = data.copy()
    data_copy = np.array(data_copy[0]).reshape((-1, 1))
    scaler = MinMaxScaler(feature_range=(options.get('feature_range_min'), options.get('feature_range_max')))
    scaler.fit(data_copy)
    data_copy = scaler.transform(data_copy).flatten()

    return np.array([data_copy, data[1]])


def get_config():
    return {
        'modalities': ['serial/*', 'positional/2d'],
        'doc': 'Трансформировать данные путем масштабирования значений под указанный диапазон',
        'arguments': {
            'feature_range_min': {
                'doc': 'Минимальное значение',
                'type': 'number'
            },
            'feature_range_max': {
                'doc': 'Максимальное значение',
                'type': 'number'
            }
        }
    }
