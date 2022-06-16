import serial
import time

from .device import Device


class ArduinoUNO(Device):
    default_port = '/dev/ttyACM0'
    default_baudrate = 115200

    def __init__(self, options):
        super().__init__(options)
        self.board = None
        self.port = options.get('port') or ArduinoUNO.default_port
        self.baudrate = options.get('baudrate') or ArduinoUNO.default_baudrate
        self.modality = 'serial/ecg'
        self.sampling_rate = 330

    def start(self):
        super(ArduinoUNO, self).start()

    def run(self):
        self.board = serial.Serial(self.port, self.baudrate)
        time.sleep(2)  # необходима пара секунд для инициализации порта
        if not self.board.isOpen():
            raise Exception("Can't connect to Arduino port")

        i = 0
        while self.is_started():
            if self.board is None:
                pass
            if self.board.inWaiting() == 0:
                pass

            try:
                line = self.board.readline()
                data = int(line.decode().rstrip())
                t = time.time()
                board_data = [
                    [data],
                    [t]
                ]
                i += 1

                self.buffer.put((board_data, True))
            except UnicodeDecodeError:
                pass
            except ValueError:
                pass

        self.board.close()
        self.board = None

    def stop(self):
        super(ArduinoUNO, self).stop()

    def format_to_sse(self, data):
        return data

    def should_save_data(self, data):
        return True
