from cv2 import cv2
from .device import Device


class Camera(Device):
    default_width = 600
    default_height = 450

    def __init__(self):
        super().__init__()
        self.cap = None
        self.width = Camera.default_width
        self.height = Camera.default_height
        self.last_frame = None

    def start_record(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        super(Camera, self).start_record()

    def run(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                self.last_frame = buffer.tobytes()

    def pause_record(self):
        pass

    def stop_record(self):
        super(Camera, self).stop_record()

        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def get_data(self):
        super(Camera, self).get_data()
        return self.last_frame
