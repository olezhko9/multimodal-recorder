import numpy as np


def run(data, options, device):
    data_copy = data.copy()
    max_value = np.max(data_copy[0])
    data_copy[0] = data_copy[0] * -1 + max_value

    return data_copy


def get_config():
    return {
        'modalities': ['serial/ecg'],
        'doc': 'Перевернуть сигнал ЭКГ',
        'arguments': {}
    }
