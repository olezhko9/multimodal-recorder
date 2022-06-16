import numpy as np
import pandas as pd

from scipy.signal import find_peaks
import matplotlib.pyplot as plt


def run(data, options, device):
    cardio_data = data[0]
    peaks, _ = find_peaks(pd.Series(cardio_data), height=options.get('height'), distance=options.get('distance'))

    peak_times = data[1][peaks]
    cardio_intervals = []
    last_peak_time = peak_times[0]
    for peak in peak_times:
        cardio_intervals.append(np.round((peak - last_peak_time) * 1000))
        last_peak_time = peak

    plt.plot(cardio_data)
    plt.plot(peaks, cardio_data[peaks], 'o')
    plt.show()

    return np.array([cardio_intervals[1:], peak_times[1:]])


def get_config():
    return {
        'modalities': ['serial/ecg'],
        'doc': 'Перевести ЭКГ сигнал в кардиоинтервалы',
        'arguments': {
            'height': {
                'doc': 'Минимальная высотка пика',
                'type': 'number'
            },
            'distance': {
                'doc': 'Минимальное расстояние между соседними пиками',
                'type': 'number'
            }
        }
    }
