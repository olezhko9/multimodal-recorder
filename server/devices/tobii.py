import time
import traceback

import numpy as np

from .device import Device


class Tobii(Device):
    def __init__(self, options):
        super().__init__(options)
        self.eye_tracker = None
        self.modality = 'positional/2d'
        self.sampling_rate = 30

    def start(self):
        super(Tobii, self).start()

    def run(self):
        def gaze_data_callback(gaze_data):
            t = time.time()
            data = [
                [gaze_data['left_gaze_point_on_display_area'][0]],
                [gaze_data['left_gaze_point_on_display_area'][1]],
                [gaze_data['right_gaze_point_on_display_area'][0]],
                [gaze_data['right_gaze_point_on_display_area'][1]],
                [t],
            ]

            if np.isnan(data[0][0]) or np.isnan(data[1][0]) or np.isnan(data[2][0]) or np.isnan(data[3][0]):
                return

            self.buffer.put((data, True))

        try:
            import tobii_research as tr
            found_eyetrackers = tr.find_all_eyetrackers()
            self.eye_tracker = found_eyetrackers[0]
            print("Address: " + self.eye_tracker.address)
            print("Model: " + self.eye_tracker.model)
            print("Name (It's OK if this is empty): " + self.eye_tracker.device_name)
            print("Serial number: " + self.eye_tracker.serial_number)

            self.eye_tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
        except Exception:
            traceback.print_exc()

        while self.is_started():
            time.sleep(0.2)

        if self.eye_tracker:
            self.eye_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

    def stop(self):
        super(Tobii, self).stop()

    def format_to_sse(self, data):
        return data
