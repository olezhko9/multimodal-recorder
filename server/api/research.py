from flask import Blueprint, request, jsonify
from service import research_service


def get_research_api():
    router = Blueprint('research_router', __name__)

    @router.route("/research")
    def research_get():
        res = research_service.get_researches()
        return jsonify(res)

    @router.route("/research", methods=['POST'])
    def research_post():
        research_data = request.json
        res = research_service.create_research(research_data)
        return jsonify(res)

    @router.route("/research/<research_id>", methods=['DELETE'])
    def research_delete(research_id):
        research_service.delete_research(research_id)
        return jsonify(True)

    @router.route("/research/<research_id>/records", methods=['GET'])
    def get_research_records(research_id):
        res = research_service.get_records(research_id)
        return jsonify(res)

    return router
