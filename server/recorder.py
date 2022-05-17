import threading
import time
import pathlib
import numpy as np
import utils.flie_system as fs

from cv2 import cv2
from config import config


class DataRecorder(threading.Thread):
    def __init__(self, device_manager):
        threading.Thread.__init__(self)
        self.device_manager = device_manager
        self.data_stream = None
        self._recording = False
        self.base_path = ''

    def start_record(self, research_id, record_id):
        devices = self.device_manager.get_devices()
        self.data_stream = self.device_manager.get_data_stream()

        if not self.data_stream:
            raise Exception('Devices data stream is not defined')

        data_dir = config.get('data_dir')
        self.base_path = f'{data_dir}/{research_id}/{record_id}'

        for device in devices:
            fs.create_directory(f'{self.base_path}/{device}')

        if not self.is_alive():
            self._recording = True
            threading.Thread.start(self)
            return True

        return False

    def stop_record(self):
        self._recording = False
        self.base_path = ''

    def run(self):
        now_string = str(round(time.time() * 1000))

        while True:
            if not self._recording:
                return

            device_id, data = self.data_stream.get()
            if device_id == 'camera':
                name = "frame_" + str(round(time.time() * 1000))
                cv2.imwrite(f'{self.base_path}/{device_id}/{name}.jpg', data)
            elif device_id == 'openbci_cython':
                data = np.transpose(data)
                with open(f'{self.base_path}/{device_id}/{now_string}.csv', 'a') as csv_file:
                    np.savetxt(csv_file, data, delimiter=',', fmt='%f')

    def is_recording(self):
        return self._recording
