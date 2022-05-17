from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import connect

from service import device_service
from api import device_api, research_api
from devices import DeviceManager
from recorder import DataRecorder
from utils import MongoJsonEncoder
import utils.flie_system as fs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000", "http://localhost:3000"]}})

connect(host="mongodb://localhost:27017/test")
app.json_encoder = MongoJsonEncoder

device_manager = DeviceManager(all_devices=device_service.get_devices())
data_recorder = DataRecorder(device_manager)

app.register_blueprint(device_api(device_manager))
app.register_blueprint(research_api())


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


@app.route('/fs/directory/open', methods=['POST'])
def fs_open_dir():
    params = request.json
    res = fs.open_directory(params.get('directory', None))
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
