from time import sleep

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds, BrainFlowError
from utils.logger import logging

from .device import Device

import numpy as np


class OpenBCIBoard(Device):
    default_port = "/dev/ttyUSB0"

    def __init__(self, options):
        super().__init__(options)
        BoardShim.enable_dev_board_logger()

        port = options.get('port') or OpenBCIBoard.default_port
        params = BrainFlowInputParams()
        params.serial_port = port

        board_type = options.get('board_type')
        if board_type == 'Cyton':
            self.board_id = BoardIds.CYTON_DAISY_BOARD.value
        elif board_type == 'Synthetic':  # use synthetic board for demo
            self.board_id = BoardIds.SYNTHETIC_BOARD.value

        self.board = BoardShim(self.board_id, params)

        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.timestamp_channel = self.board.get_timestamp_channel(self.board_id)
        self.eeg_channels = self.board.get_eeg_channels(self.board_id)
        print('board eeg channels:', self.eeg_channels)
        print('board timestamp channel:', self.timestamp_channel)
        self.channels = np.append(self.eeg_channels, self.timestamp_channel)

        self.buffer = None
        self.max_buffer_size = self.sampling_rate // 4

    def start_record(self):
        logging.info("Board start")
        if not self.board.is_prepared():
            self.board.prepare_session()
            self.board.start_stream()
            BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')

        super(OpenBCIBoard, self).start_record()

    def run(self):
        pass
        # while self.pause_flag.is_set():
        #     data = self.board.get_current_board_data(1)
        #     timestamp = int(data[self.timestamp_channel][0])

    def pause_record(self):
        logging.info("Board pause")

    def stop_record(self):
        logging.info("Board stop")
        super(OpenBCIBoard, self).stop_record()
        try:
            self.board.stop_stream()
        except BrainFlowError:
            logging.error("Stream already stopped")

        self.board.release_session()

    def get_data(self):
        # берем все данные из платы и удаляем их из буфера платы
        board_data = self.board.get_board_data()

        if len(board_data[0]):
            board_data = board_data[self.channels]

            if self.buffer is None:
                self.buffer = board_data
            else:
                self.buffer = np.concatenate((self.buffer, board_data), axis=1)
                if len(self.buffer[0]) > self.max_buffer_size:
                    buffer = self.buffer
                    self.buffer = None

                    return buffer, self.should_save_data(buffer)

        return None, False

    def format_to_sse(self, data):
        return data.tolist()

    def should_save_data(self, data):
        return True


if __name__ == '__main__':
    board = OpenBCIBoard({})
    board.start()
    sleep(2)
    data = board.get_data()
    print(data)
