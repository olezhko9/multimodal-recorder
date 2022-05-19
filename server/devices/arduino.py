import numpy as np
import serial
import time

from .device import Device


class ArduinoUNO(Device):
    default_port = '/dev/ttyACM0'
    default_baudrate = 9600

    def __init__(self, options):
        super().__init__(options)
        self.board = None
        self.port = options.get('port') or ArduinoUNO.default_port
        self.baudrate = options.get('baudrate') or ArduinoUNO.default_baudrate
        self.buffer = None
        self.max_buffer_size = 50

    def start(self):
        self.board = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=0.05)
        time.sleep(2)  # необходима пара секунд для инициализации порта
        if not self.board.isOpen():
            raise Exception("Can't connect to Arduino port")

        super(ArduinoUNO, self).start()

    def run(self):
        while True:
            if self.board is None:
                pass
            if self.board.inWaiting() == 0:
                pass

            try:
                data = int(self.board.readline().decode().rstrip())
                board_data = [
                    [data],
                    [time.time()]
                ]

                if self.buffer is None or len(self.buffer[0]) > self.max_buffer_size:
                    self.buffer = np.array(board_data)
                else:
                    self.buffer = np.concatenate((self.buffer, board_data), axis=1)
            except UnicodeDecodeError:
                pass

    def pause(self):
        pass

    def stop(self):
        super(ArduinoUNO, self).stop()
        self.board.close()
        self.buffer = None
        self.board = None

    def get_data(self):
        super(ArduinoUNO, self).get_data()

        if self.buffer is not None and len(self.buffer[0]) > self.max_buffer_size:
            buffer = self.buffer
            self.buffer = None
            return buffer, self.should_save_data(buffer)

        return None, False

    def format_to_sse(self, data):
        return data.tolist()

    def should_save_data(self, data):
        return True
