import time

from eeg_board import EEGBoard
from flask import Flask, Response, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/stream")
def eeg_stream():
    def stream_board_data():
        board = EEGBoard()
        board.start()
        event = "eeg_update"

        buffer_last_seconds = 2
        buffer_size = buffer_last_seconds * board.sampling_rate
        updates_per_second = 5

        while True:
            time.sleep(1 / updates_per_second)
            data = board.get_data()
            if len(data[0]) != 0:
                print(len(data), len(data[0]))
                data = data[-buffer_size:]
                yield f"event:{event}\ndata:{data.tolist()}\n\n"

    return Response(stream_board_data(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
