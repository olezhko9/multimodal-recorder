from time import sleep

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds, BrainFlowError
from utils.logger import logging


class EEGBoard(object):
    def __init__(self):
        super().__init__()
        BoardShim.enable_dev_board_logger()
        # self.pause_flag = threading.Event()

        # use synthetic board for demo
        port = "/dev/ttyUSB0"
        params = BrainFlowInputParams()
        params.serial_port = port
        self.board_id = BoardIds.SYNTHETIC_BOARD.value
        # self.board_id = BoardIds.CYTON_DAISY_BOARD.value
        self.board = BoardShim(self.board_id, params)

        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.timestamp_channel = self.board.get_timestamp_channel(self.board_id)
        self.eeg_channels = self.board.get_eeg_channels(self.board_id)
        # print(self.sampling_rate, self.eeg_channels, self.timestamp_channel)

    def start(self):
        logging.info("Board start")
        # self.pause_flag.set()
        if not self.board.is_prepared():
            self.board.prepare_session()
            self.board.start_stream()
            BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')

    def run(self):
        pass
        # while self.pause_flag.is_set():
        #     data = self.board.get_current_board_data(1)
        #     timestamp = int(data[self.timestamp_channel][0])

    def pause(self):
        logging.info("Board pause")
        # self.pause_flag.clear()
        # self.board.stop_stream()

    def stop(self):
        logging.info("Board stop")
        # self.pause_flag.clear()
        try:
            self.board.stop_stream()
        except BrainFlowError:
            logging.error("Stream already stopped")

        self.board.release_session()

    def get_data(self):
        return self.board.get_board_data()


if __name__ == '__main__':
    board = EEGBoard()
    board.start()
    sleep(2)
    data = board.get_data()
    print(data)
