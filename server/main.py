import json

from flask import Flask, Response, request, jsonify
from flask_cors import CORS

from devices import DeviceManager
from recorder import DataRecorder


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000", "http://localhost:3000"]}})

device_manager = DeviceManager()
data_recorder = DataRecorder(device_manager)


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

        device_manager.read_data()
        data_recorder.start_record()
    except Exception as err:
        print(err)
        data_recorder.stop_record()
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
    data_recorder.stop_record()
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

    device_manager.start_stream(device_id)

    def generator():
        while True:
            try:
                item_device_id, data = device_manager.stream_queue.get()
                if item_device_id == 'camera':
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
                elif item_device_id == 'openbci_cython':
                    yield f"event:{'upd'}\ndata:{data}\n\n"
            except GeneratorExit:
                device_manager.stop_stream(device_id)
                return

    return Response(generator(), mimetype=mimetype)


if __name__ == "__main__":
    app.run(debug=True)
