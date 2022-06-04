from flask import Blueprint, request, jsonify
from os.path import isdir, join
from service import record_service
from config import config

import utils.flie_system as fs
import traceback


def get_record_api(device_manager, record_manager):
    router = Blueprint('record_router', __name__)

    @router.route("/research/<research_id>/subject/<subject_id>/record", methods=['GET'])
    def get_research_records(research_id, subject_id):
        records = record_service.get_records(research_id, subject_id)
        _records = []
        for record in records:
            record_dir_name = record_service.get_record_dir(record['_id'])
            record['directory'] = record_dir_name

            notebooks_dir = config.get('notebooks_dir', None)
            record['notebooks_directory'] = join(notebooks_dir, 'record_' + str(record['_id']))

        return jsonify(records)

    @router.route("/record/start", methods=['POST'])
    def start_record():
        record_data = request.json
        research_id = record_data['research_id']
        subject_id = record_data['subject_id']
        try:
            if record_manager.is_recording():
                return "Recording already started", 500

            record = record_service.create_record(research_id, subject_id)
            if record:
                record_dir = record_service.get_record_dir(record['_id'])
                fs.create_directory(record_dir)
                device_modality_dict = record_manager.start_record(record['_id'], record_dir)
                record_service.set_record_data(record['_id'], device_modality_dict)

            return jsonify(record)
        except Exception:
            traceback.print_exc()
            record_manager.stop_record()
            device_manager.stop_and_remove_devices()
            return "Error when trying connect to device", 500

    @router.route("/record/stop", methods=['POST'])
    def stop_record():
        record_manager.stop_record()
        return jsonify(True)

    @router.route('/record/<record_id>', methods=['DELETE'])
    def delete_record(record_id):
        record = record_service.get_record(record_id)
        if record:
            record_dir = record_service.get_record_dir(record_id)
            fs.delete_directory(record_dir)
            record_service.delete_record(record_id)
        return jsonify(True)

    @router.route('/record/<record_id>', methods=['GET'])
    def get_record(record_id):
        record = record_service.get_record(record_id)
        record_dir_name = record_service.get_record_dir(record_id)
        record_dir = fs.list_directory(record_dir_name)
        devices = [f for f in record_dir if isdir(join(record_dir_name, f))]
        record = dict(**record, devices=devices)
        return jsonify(record)

    # @router.route("/record/pause", methods=['POST'])
    # def pause_record():
    #     return jsonify(True)
    #
    # @router.route("/record/unpause", methods=['POST'])
    # def unpause_record():
    #     return jsonify(True)

    return router
