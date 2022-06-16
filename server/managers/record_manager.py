import json
import threading
import time
import numpy as np
import utils.flie_system as fs

from cv2 import cv2


class RecordManager(threading.Thread):
    def __init__(self, device_manager):
        threading.Thread.__init__(self)
        self.device_manager = device_manager
        self.data_stream = None
        self._recording = False
        self.record_dir = ''
        self.last_event = None
        self.files = {}

    def start_record(self, record_id, record_dir):
        devices = self.device_manager.get_devices()
        self.data_stream = self.device_manager.get_data_stream()

        if not self.data_stream:
            raise Exception('Devices data stream is not defined')

        self.record_dir = record_dir
        now_string = str(round(time.time() * 1000))
        meta = {
            'record_id': record_id,
            'device': {},
            'subject': {}
        }

        device_modality_dict = {}
        devices_id = [device_id for device_id in devices]
        devices_id.append('events')
        for device_id in devices_id:
            fs.create_directory(f'{self.record_dir}/{device_id}')
            modality = 'events'
            if device_id != 'events':
                modality = devices[device_id].modality
            device_modality_dict[device_id] = modality

            meta['modality'] = modality
            meta['device']['device_id'] = device_id

            if not modality.startswith('visual') and not modality.startswith('audio'):
                self.files[device_id] = open(f'{self.record_dir}/{device_id}/{device_id}_{now_string}.txt', 'a')
                self.files[device_id].write(json.dumps(meta, default=str) + '\n')

        self._recording = True
        if not self.is_alive():
            threading.Thread.start(self)

        return device_modality_dict

    def stop_record(self):
        self._recording = False
        self.record_dir = ''
        self.last_event = None
        self.files = {}

    def run(self):
        while True:
            if not self._recording:
                continue

            device_id, data = self.data_stream.get()
            modality = self.device_manager.get_device(device_id).modality
            if modality == 'visual/image':
                name = "frame_" + str(round(time.time() * 1000))
                cv2.imwrite(f'{self.record_dir}/{device_id}/{name}.jpg', data)
            elif modality.startswith('serial/') or modality.startswith('positional/'):
                data = np.transpose(data)
                if self.record_dir:
                    np.savetxt(self.files[device_id], data, delimiter=',', fmt='%f')
            else:
                print(f'Modality for device {device_id} not defined')

            device_id = 'events'
            if self.last_event is not None:
                data = [self.last_event[0], json.dumps(self.last_event[1]), time.time()]
                if self.record_dir:
                    self.files[device_id].write(','.join(str(val) for val in data) + '\n')

                self.last_event = None

    def is_recording(self):
        return self._recording

    def set_last_event(self, event_name, event_data):
        if event_data is None:
            event_data = ''
        else:
            event_data = json.dumps(event_data, indent=None)

        self.last_event = (event_name, event_data)
