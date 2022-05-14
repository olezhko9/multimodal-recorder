import time
import json

from flask import Flask, Response, request, jsonify
from flask_cors import CORS

from devices import DeviceManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000", "http://localhost:3000"]}})

device_manager = DeviceManager()


@app.route("/devices")
def devices():
    with open("./devices.json") as devices_json:
        return jsonify(json.load(devices_json))


@app.route("/record/start", methods=['POST'])
def start_record():
    request_devices = request.json
    try:
        for device in request_devices:
            device_id = device['id']

            device_params = {}
            if device.get('settings'):
                for param in device['settings']:
                    device_params[param['name']] = param['value']

            device_manager.add_and_run_device(device_id, device_params)
    except Exception:
        device_manager.stop_and_remove_devices()
        return "Error when trying to connect to device", 500

    return jsonify(True)


@app.route("/record/pause", methods=['POST'])
def pause_record():
    return jsonify(True)


@app.route("/record/unpause", methods=['POST'])
def unpause_record():
    return jsonify(True)


@app.route("/record/stop", methods=['POST'])
def stop_record():
    device_manager.stop_and_remove_devices()
    return jsonify(True)


@app.route("/stream")
def stream():
    device_id = request.args.get('device')

    device = device_manager.get_device(device_id)
    mimetype = 'text/event-stream'

    if device is None:
        return 'Invalid device id', 500

    if device_id == 'camera':
        mimetype = 'multipart/x-mixed-replace; boundary=frame'
    elif device_id == 'openbci_cython':
        mimetype = 'text/event-stream'
        buffer_last_seconds = 2
        buffer_size = buffer_last_seconds * device.sampling_rate
        updates_per_second = 5

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
                return

    return Response(gen_frames(), mimetype=mimetype)


if __name__ == "__main__":
    app.run(debug=True)
