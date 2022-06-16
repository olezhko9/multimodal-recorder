import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes


def run(data, options, device):
    data = np.copy(data)
    options['sampling_rate'] = device.get_sampling_rate()
    options['filter_type'] = FilterTypes[options['filter_type']].value
    DataFilter.perform_wavelet_denoising(data=data, **options)
    return data


def get_config():
    return {
        'modalities': ['serial/eeg'],
        'doc': 'Удаляет шумы при помощи вейвлет-преобразования',
        'arguments': {
            'wavelet': {
                'type': 'string',
                'doc': 'supported vals: db1..db15, haar, sym2..sym10, coif1..coif5, bior1.1, bior1.3, bior1.5, bior2.2, bior2.4, ior2.6, bior2.8, bior3.1, bior3.3, bior3.5, bior3.7, bior3.9, bior4.4, bior5.5, bior6.8'
            },
            'decomposition_level': 'number'
        }
    }
