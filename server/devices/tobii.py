import time
import traceback
import tobii_research as tr

from .device import Device


class Tobii(Device):
    def __init__(self, options):
        super().__init__(options)
        self.eye_tracker = None

    def start(self):
        super(Tobii, self).start()

    def gaze_data_callback(self, gaze_data):
        t = time.time()
        data = [
            [gaze_data['left_gaze_point_on_display_area'][0]],
            [gaze_data['left_gaze_point_on_display_area'][1]],
            [gaze_data['right_gaze_point_on_display_area'][0]],
            [gaze_data['right_gaze_point_on_display_area'][1]],
            [t],
        ]

        self.buffer.put((data, True))

    def run(self):
        try:
            found_eyetrackers = tr.find_all_eyetrackers()
            self.eye_tracker = found_eyetrackers[0]
            print("Address: " + self.eye_tracker.address)
            print("Model: " + self.eye_tracker.model)
            print("Name (It's OK if this is empty): " + self.eye_tracker.device_name)
            print("Serial number: " + self.eye_tracker.serial_number)
            self.eye_tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)
        except Exception:
            traceback.print_exc()

        while self.is_started():
            time.sleep(1)

        self.eye_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)

    def stop(self):
        super(Tobii, self).stop()
