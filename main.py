import time

from eeg_board import EEGBoard
from flask import Flask, Response
from flask_cors import CORS
from cv2 import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000"]}})


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


@app.route("/camera_stream")
def camera_stream():
    camera = cv2.VideoCapture(0)

    def gen_frames():
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
