import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes


def run(data, options, device):
    data = np.copy(data)
    options['sampling_rate'] = device['sampling_rate']
    options['filter_type'] = FilterTypes[options['filter_type']].value
    for i in range(0, 16):
        DataFilter.perform_bandstop(data=data[i], **options)

    return data


def get_config():
    return {
        'modalities': ['serial/eeg'],
        'doc': 'Применяет полосный фильтр частот',
        'arguments': {
            'center_freq': {
                'doc': 'Центральная частота',
                'type': 'number',
                'default': 30
            },
            'band_width': {
                'type': 'number',
                'doc': 'Ширина полосы'
            },
            'order': 'number',
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
