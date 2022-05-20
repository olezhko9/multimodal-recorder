from flask import Blueprint, request, jsonify
from service import subject_service

import utils.flie_system as fs
import traceback


def get_subject_api():
    router = Blueprint('subject_router', __name__)

    @router.route("/research/<research_id>/subject", methods=['GET'])
    def get_research_subjects(research_id):
        res = [
            dict(**subject, directory=subject_service.get_subject_dir(research_id, subject['_id']))
            for subject in subject_service.get_subjects(research_id)
        ]
        return jsonify(res)

    @router.route("/research/<research_id>/subject", methods=['POST'])
    def create_subject(research_id):
        subject_data = request.json
        subject = subject_service.create_subject(research_id, subject_data)
        if subject:
            fs.create_directory(subject_service.get_subject_dir(research_id, subject['_id']))
        return jsonify(subject)

    @router.route('/subject/<subject_id>', methods=['DELETE'])
    def delete_subject(subject_id):
        subject = subject_service.get_subject(subject_id)
        if subject:
            subject_dir = subject_service.get_subject_dir(subject['research_id'], subject_id)
            fs.delete_directory(subject_dir)
            subject_service.delete_subject(subject_id)
            return jsonify(True)
        return jsonify(False)

    return router
