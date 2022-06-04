import numpy as np
import time

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds, BrainFlowError
from utils.logger import logging
from .device import Device


class OpenBCIBoard(Device):
    default_port = "/dev/ttyUSB0"

    def __init__(self, options):
        super().__init__(options)
        BoardShim.enable_dev_board_logger()

        self.port = options.get('port') or OpenBCIBoard.default_port
        self.board_type = options.get('board_type')

        if self.board_type == 'Cyton':
            self.board_id = BoardIds.CYTON_DAISY_BOARD.value
        elif self.board_type == 'Synthetic':  # use synthetic board for demo
            self.board_id = BoardIds.SYNTHETIC_BOARD.value

        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.modality = 'serial/eeg'

    def start(self):
        self.input_params = BrainFlowInputParams()
        self.input_params.serial_port = self.port

        super(OpenBCIBoard, self).start()

    def run(self):
        self.board = BoardShim(self.board_id, self.input_params)

        self.timestamp_channel = self.board.get_timestamp_channel(self.board_id)
        self.eeg_channels = self.board.get_eeg_channels(self.board_id)
        print('board type', self.board_type)
        print('board eeg channels:', self.eeg_channels)
        print('board timestamp channel:', self.timestamp_channel)
        print('board sampling_rate', self.sampling_rate)
        self.channels = np.append(self.eeg_channels, self.timestamp_channel)

        logging.info("Board start")
        if not self.board.is_prepared():
            self.board.prepare_session()
            self.board.start_stream()
            BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')

        while self.is_started():
            try:
                # берем все данные из платы и удаляем их из буфера платы
                board_data = self.board.get_board_data()

                if len(board_data[0]):
                    board_data = board_data[self.channels]
                    self.buffer.put((board_data, self.should_save_data(board_data)))

                time.sleep(0.1)
            except Exception as e:
                print(e)

        try:
            self.board.stop_stream()
        except BrainFlowError:
            logging.error("Stream already stopped")

        self.board.release_session()

    def stop(self):
        logging.info("Board stop")
        super(OpenBCIBoard, self).stop()

    def format_to_sse(self, data):
        return data.tolist()

    def should_save_data(self, data):
        return True
