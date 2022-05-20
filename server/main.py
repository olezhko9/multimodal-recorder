from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import connect
from os.path import isfile, isdir, join

from service import device_service
from api import device_api, research_api, record_api, subject_api
from device_manager import DeviceManager
from record_manager import RecordManager
from utils import MongoJsonEncoder
from config import config

import utils.flie_system as fs

app = Flask(__name__, static_folder='frames', static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

CORS(app, resources={r"/*": {"origins": [
    "http://127.0.0.1:3000", "http://localhost:3000",
    "http://127.0.0.1:5000", "http://localhost:5000"
]}})

connect(host="mongodb://localhost:27017/test")
app.json_encoder = MongoJsonEncoder

device_manager = DeviceManager(all_devices=device_service.get_devices())
record_manager = RecordManager(device_manager)

app.register_blueprint(device_api(device_manager))
app.register_blueprint(research_api())
app.register_blueprint(record_api(device_manager, record_manager))
app.register_blueprint(subject_api())


@app.route('/fs/directory/open', methods=['POST'])
def fs_open_dir():
    params = request.json
    res = fs.open_directory(params.get('directory', None))
    return jsonify(res)


@app.route('/event', methods=['POST'])
def put_event():
    event = request.json
    if event.get('name'):
        record_manager.set_last_event(event['name'], event.get('data'))
    return jsonify(True)


@app.route('/notebook', methods=["GET"])
def get_notebooks():
    notebooks_dir = './notebooks/original'
    notebooks = [f for f in fs.list_directory(notebooks_dir) if f.endswith('.ipynb') and isfile(join(notebooks_dir, f))]
    return jsonify(notebooks)


@app.route("/frame")
def get_frames():
    frames_dir = config.get("frames_dir")
    frames_dir_files = fs.list_directory(frames_dir)
    frames = []
    for file in frames_dir_files:
        path = join(frames_dir, file)

        if not isdir(path):
            continue

        frame_files = fs.list_directory(path)
        if 'index.html' in frame_files:
            frames.append(file)

    return jsonify(frames)


@app.errorhandler(Exception)
def handle_exception(err):
    return str(err), 500


if __name__ == "__main__":
    app.run(debug=True)
