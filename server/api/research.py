from flask import Blueprint, request, jsonify
from service import research_service

import utils.flie_system as fs


def get_research_api():
    router = Blueprint('research_router', __name__)

    @router.route("/research")
    def get_researches():
        res = research_service.get_researches()
        return jsonify(res)

    @router.route("/research", methods=['POST'])
    def create_research():
        research_data = request.json
        res = research_service.create_research(research_data)
        return jsonify(res)

    @router.route("/research/<research_id>", methods=['DELETE'])
    def delete_research(research_id):
        research_dir = research_service.get_research_dir(research_id)
        fs.delete_directory(research_dir)

        research_service.delete_research(research_id)
        return jsonify(True)

    return router
