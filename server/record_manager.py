import json
import threading
import time
import numpy as np
import utils.flie_system as fs

from cv2 import cv2
from csv import writer
from config import config


class RecordManager(threading.Thread):
    def __init__(self, device_manager):
        threading.Thread.__init__(self)
        self.device_manager = device_manager
        self.data_stream = None
        self._recording = False
        self.base_path = ''
        self.last_event = None

    def start_record(self, research_id, record_id):
        devices = self.device_manager.get_devices()
        self.data_stream = self.device_manager.get_data_stream()

        if not self.data_stream:
            raise Exception('Devices data stream is not defined')

        data_dir = config.get('data_dir')
        self.base_path = f'{data_dir}/{research_id}/{record_id}'

        for device in devices:
            fs.create_directory(f'{self.base_path}/{device}')

        fs.create_directory(f'{self.base_path}/events')

        if not self.is_alive():
            self._recording = True
            threading.Thread.start(self)
            return True

        return False

    def stop_record(self):
        self._recording = False
        self.base_path = ''
        self.last_event = None

    def run(self):
        now_string = str(round(time.time() * 1000))

        while True:
            if not self._recording:
                continue

            device_id, data = self.data_stream.get()
            if device_id == 'camera':
                name = "frame_" + str(round(time.time() * 1000))
                cv2.imwrite(f'{self.base_path}/{device_id}/{name}.jpg', data)
            elif device_id == 'openbci_cython' or device_id == 'arduino_uno':
                data = np.transpose(data)
                if self.base_path:
                    with open(f'{self.base_path}/{device_id}/{now_string}.csv', 'a') as csv_file:
                        np.savetxt(csv_file, data, delimiter=',', fmt='%f')

            if self.last_event is not None:
                device_id = 'events'
                data = [self.last_event[0], self.last_event[1], time.time()]
                with open(f'{self.base_path}/{device_id}/{now_string}.csv', 'a') as csv_file:
                    writer_object = writer(csv_file)
                    writer_object.writerow(data)
                    csv_file.close()

                self.last_event = None

    def is_recording(self):
        return self._recording

    def set_last_event(self, event_name, event_data):
        if event_data is None:
            event_data = ''
        else:
            event_data = json.dumps(event_data, indent=None)

        self.last_event = (event_name, event_data)
