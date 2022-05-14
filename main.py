import time
import json

from flask import Flask, Response, request, jsonify
from flask_cors import CORS

from devices import *

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
def stream():
    device_id = request.args.get('device')

    device = None
    mimetype = 'text/event-stream'

    if device_id == 'camera':
        device = Camera()
        mimetype = 'multipart/x-mixed-replace; boundary=frame'
    elif device_id == 'openbci_cython':
        device = EEGBoard()
        mimetype = 'text/event-stream'
        buffer_last_seconds = 2
        buffer_size = buffer_last_seconds * device.sampling_rate
        updates_per_second = 5

    if device is None:
        return 'Invalid device', 500

    device.start_record()

    def gen_frames():
        while True:
            try:
                if device_id == 'camera':
                    data = device.get_data()
                    if data:
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
                elif device_id == 'openbci_cython':
                    time.sleep(1 / updates_per_second)
                    data = device.get_data()
                    if len(data[0]) != 0:
                        print(len(data), len(data[0]))
                        data = data[-buffer_size:]
                        yield f"event:{'upd'}\ndata:{data.tolist()}\n\n"
            except GeneratorExit:
                print(f'Device [{device_id}] stream closed')
                device.stop_record()
                return

    return Response(gen_frames(), mimetype=mimetype)


if __name__ == "__main__":
    app.run(debug=True)
