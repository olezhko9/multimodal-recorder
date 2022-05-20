import json
import threading
import time
import numpy as np
import utils.flie_system as fs

from cv2 import cv2
from csv import writer


class RecordManager(threading.Thread):
    def __init__(self, device_manager):
        threading.Thread.__init__(self)
        self.device_manager = device_manager
        self.data_stream = None
        self._recording = False
        self.record_dir = ''
        self.last_event = None

    def start_record(self, record_dir):
        devices = self.device_manager.get_devices()
        self.data_stream = self.device_manager.get_data_stream()

        if not self.data_stream:
            raise Exception('Devices data stream is not defined')

        self.record_dir = record_dir

        for device in devices:
            fs.create_directory(f'{self.record_dir}/{device}')

        fs.create_directory(f'{self.record_dir}/events')

        if not self.is_alive():
            self._recording = True
            threading.Thread.start(self)
            return True

        return False

    def stop_record(self):
        self._recording = False
        self.record_dir = ''
        self.last_event = None

    def run(self):
        now_string = str(round(time.time() * 1000))

        while True:
            if not self._recording:
                continue

            device_id, data = self.data_stream.get()
            if device_id == 'camera':
                name = "frame_" + str(round(time.time() * 1000))
                cv2.imwrite(f'{self.record_dir}/{device_id}/{name}.jpg', data)
            elif device_id == 'openbci_cython' or device_id == 'arduino_uno':
                data = np.transpose(data)
                if self.record_dir:
                    with open(f'{self.record_dir}/{device_id}/{now_string}.csv', 'a') as csv_file:
                        np.savetxt(csv_file, data, delimiter=',', fmt='%f')

            if self.last_event is not None:
                device_id = 'events'
                data = [self.last_event[0], self.last_event[1], time.time()]
                with open(f'{self.record_dir}/{device_id}/{now_string}.csv', 'a') as csv_file:
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
