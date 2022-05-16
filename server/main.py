from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from mongoengine import connect

from devices import DeviceManager
from recorder import DataRecorder
from utils import MongoJsonEncoder
import utils.flie_system as fs
from service import device_service, research_service

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000", "http://localhost:3000"]}})

connect(host="mongodb://localhost:27017/test")
app.json_encoder = MongoJsonEncoder

device_manager = DeviceManager(all_devices=device_service.get_devices())

data_recorder = DataRecorder(device_manager)


@app.route("/devices")
def devices():
    res = device_service.get_devices()
    return jsonify(res)


@app.route("/research")
def research_get():
    res = research_service.get_researches()
    return jsonify(res)


@app.route("/research", methods=['POST'])
def research_post():
    research_data = request.json
    res = research_service.create_research(research_data)
    return jsonify(res)


@app.route("/research/<research_id>", methods=['DELETE'])
def research_delete(research_id):
    research_service.delete_research(research_id)
    return jsonify(True)


@app.route("/research/<research_id>/records", methods=['GET'])
def get_research_records(research_id):
    res = research_service.get_records(research_id)
    return jsonify(res)


@app.route('/device/start', methods=['POST'])
def start_device():
    try:
        device = request.json
        device_id = device['device_id']

        device_params = {}
        if device.get('settings'):
            for param in device['settings']:
                device_params[param['name']] = param['value']

        device_manager.add_and_run_device(device_id, device_params)
        device_manager.read_data()
    except Exception:
        device_manager.stop_and_remove_devices()
        return "Error when trying connect to device", 500

    return jsonify(True)


@app.route('/device/stop', methods=['POST'])
def stop_device():
    try:
        device_id = request.json['device_id']
        device_manager.stop_and_remove_device(device_id)
    except:
        return "Error when trying stop device", 500

    return jsonify(True)


@app.route("/record/start", methods=['POST'])
def start_record():
    try:
        data_recorder.start_record()
    except Exception as err:
        print(err)
        data_recorder.stop_record()
        device_manager.stop_and_remove_devices()
        return "Error when trying connect to device", 500

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


@app.route('/fs/directory/open', methods=['POST'])
def fs_open_dir():
    params = request.json
    res = fs.open_directory(params.get('directory', None))
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
