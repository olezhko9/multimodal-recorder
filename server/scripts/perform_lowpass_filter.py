import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes


def run(data, options, device):
    data = np.copy(data)
    options['sampling_rate'] = device['sampling_rate']
    options['filter_type'] = FilterTypes[options['filter_type']].value
    print(options)
    for i in range(0, 16):
        DataFilter.perform_lowpass(data=data[i], **options)

    return data


def computed():
    print('computed')
    return 30


def get_config():
    return {
        'modalities': ['serial/eeg'],
        'doc': 'Применяет полосный фильтр частот',
        'arguments': {
            'cutoff': {
                'doc': 'Пропускать частотный спектр ниже этого значения',
                'type': 'number',
                'default': 50
            },
            'order': {
                'type': 'number',
                'doc': 'Порядок фильтра'
            },
            'filter_type': {
                'type': 'select',
                'options': ['BUTTERWORTH', 'CHEBYSHEV_TYPE_1', 'BESSEL'],
                'doc': 'Тип фильтра'
            },
            'ripple': {
                'type': 'number',
                'doc': 'Параметр при использовании фильтра Чебышева'
            }
        }
    }
