import pyaudio
import traceback

from devices.device import Device


class Microphone(Device):
    def __init__(self, options):
        super().__init__(options)
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.SAMPLE_WIDTH = 2
        self.modality = 'audio'

    def start(self):
        super(Microphone, self).start()

    def run(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        self.sample_width = p.get_sample_size(self.FORMAT)

        try:
            while self.is_started():
                data = stream.read(self.CHUNK)
                self.buffer.put(([data], True))
        except Exception:
            traceback.print_exc()

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        super(Microphone, self).stop()
