from flask import Blueprint, request, jsonify
from service import record_service

import utils.flie_system as fs
import traceback


def get_record_api(device_manager, data_recorder):
    router = Blueprint('record_router', __name__)

    @router.route("/research/<research_id>/record", methods=['GET'])
    def get_research_records(research_id):
        res = [
            dict(**record, directory=record_service.get_record_dir(research_id, record['_id']))
            for record in record_service.get_records(research_id)
        ]
        return jsonify(res)

    @router.route("/research/<research_id>/record/start", methods=['POST'])
    def start_record(research_id):
        try:
            if data_recorder.is_recording():
                return "Recording already started", 500

            record = record_service.create_record(research_id=research_id)
            if record:
                data_recorder.start_record(research_id, record['_id'])

            return jsonify(record)
        except Exception:
            traceback.print_exc()
            data_recorder.stop_record()
            device_manager.stop_and_remove_devices()
            return "Error when trying connect to device", 500

    @router.route("/record/stop", methods=['POST'])
    def stop_record():
        data_recorder.stop_record()
        return jsonify(True)

    @router.route('/record/<record_id>', methods=['DELETE'])
    def delete_record(record_id):
        record = record_service.get_record(record_id)
        if record:
            record_dir = record_service.get_record_dir(record['research_id'], record_id)
            fs.delete_directory(record_dir)
            record_service.delete_record(record_id)
        return jsonify(True)

    # @router.route("/record/pause", methods=['POST'])
    # def pause_record():
    #     return jsonify(True)
    #
    # @router.route("/record/unpause", methods=['POST'])
    # def unpause_record():
    #     return jsonify(True)

    return router
