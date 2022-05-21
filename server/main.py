from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import connect
from os.path import isdir, join

from service import device_service
from api import device_api, research_api, record_api, subject_api, fs_api, notebook_api
from device_manager import DeviceManager
from record_manager import RecordManager
from session_manager import SessionManager
from utils import MongoJsonEncoder
from config import config

import atexit
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
session_manager = SessionManager(device_manager, record_manager)

app.register_blueprint(device_api(device_manager))
app.register_blueprint(research_api())
app.register_blueprint(record_api(device_manager, record_manager))
app.register_blueprint(subject_api())
app.register_blueprint(fs_api())
app.register_blueprint(notebook_api())


@app.route('/event', methods=['POST'])
def put_event():
    event = request.json
    if event.get('name'):
        record_manager.set_last_event(event['name'], event.get('data'))
    return jsonify(True)


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


@app.route('/session', methods=['GET'])
def get_session():
    return jsonify(session_manager.get_session())


@app.errorhandler(Exception)
def handle_exception(err):
    return str(err), 500


# отключаем все устройства при экстренном завершении работы
def on_termination():
    record_manager.stop_record()
    device_manager.stop_and_remove_devices()


atexit.register(on_termination)

if __name__ == "__main__":
    app.run(debug=True)
