from cv2 import cv2
from .device import Device

from utils.logger import logging


class Camera(Device):
    default_width = 600
    default_height = 450
    default_fps = 10

    def __init__(self, options):
        super().__init__(options)
        self.cap = None
        self.width = options.get('width') or Camera.default_width
        self.height = options.get('height') or Camera.default_height
        self.fps = options.get('fps') or Camera.default_fps
        self.last_frame = None
        self.frame_number = 0

    def start_record(self):
        logging.info("Camera start")
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        super(Camera, self).start_record()

    def run(self):
        while True:
            if self.cap is None or not self.started:
                continue

            success, frame = self.cap.read()
            if not success:
                break
            else:
                self.last_frame = frame
                self.frame_number += 1

    def pause_record(self):
        pass

    def stop_record(self):
        logging.info("Camera stop")
        super(Camera, self).stop_record()

        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def get_data(self):
        super(Camera, self).get_data()
        frame = self.last_frame
        self.last_frame = None

        return frame, self.should_save_data(frame)

    def format_to_sse(self, data):
        ret, buffer = cv2.imencode('.jpg', data)
        return buffer.tobytes()

    def should_save_data(self, data):
        # сохраняем только каждый i-ый кадр, где i = fps
        return self.frame_number % (60 // self.fps) == 1
