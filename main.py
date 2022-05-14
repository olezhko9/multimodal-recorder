import time
import json

from flask import Flask, Response, request, jsonify
from flask_cors import CORS

from devices import EEGBoard, Camera

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000", "http://localhost:3000"]}})


@app.route("/devices")
def devices():
    with open("./devices.json") as devices_json:
        return jsonify(json.load(devices_json))


@app.route("/record/start", methods=['POST'])
def startRecord():
    return jsonify(True)


@app.route("/record/pause", methods=['POST'])
def pauseRecord():
    return jsonify(True)


@app.route("/record/unpause", methods=['POST'])
def unpauseRecord():
    return jsonify(True)


@app.route("/record/stop", methods=['POST'])
def stopRecord():
    return jsonify(True)


@app.route("/stream")
def eeg_stream():
    def stream_board_data():
        board = EEGBoard()
        board.start_record()
        event = "eeg_update"

        buffer_last_seconds = 2
        buffer_size = buffer_last_seconds * board.sampling_rate
        updates_per_second = 5

        while True:
            try:
                time.sleep(1 / updates_per_second)
                data = board.get_data()
                if len(data[0]) != 0:
                    print(len(data), len(data[0]))
                    data = data[-buffer_size:]
                    yield f"event:{event}\ndata:{data.tolist()}\n\n"
            except GeneratorExit:
                print('board closed')
                board.stop_record()
                return

    return Response(stream_board_data(), mimetype="text/event-stream")


@app.route("/camera_stream")
def camera_stream():
    print(50)
    print(request.data)
    print(request.get_json())
    print(request.json)
    print(request.query_string)  # b'device=camera
    print(request.url)  # http://127.0.0.1:5000/camera_stream?device=camera

    def gen_frames():
        camera = Camera()
        camera.start_record()
        while True:
            try:
                data = camera.get_data()
                if data:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
            except GeneratorExit:
                print('closed')
                camera.stop_record()
                return

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
