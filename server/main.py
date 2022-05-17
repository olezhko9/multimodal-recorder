from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import connect

from service import device_service
from api import device_api, research_api, record_api
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
app.register_blueprint(record_api(device_manager, data_recorder))


@app.route('/fs/directory/open', methods=['POST'])
def fs_open_dir():
    params = request.json
    res = fs.open_directory(params.get('directory', None))
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
