from flask import Blueprint, request, jsonify

import utils.flie_system as fs


def get_api():
    router = Blueprint('fs_router', __name__)

    @router.route('/fs/directory/open', methods=['POST'])
    def fs_open_dir():
        params = request.json
        res = fs.open_directory(params.get('directory', None))
        return jsonify(res)

    @router.route('/fs/directory/remove', methods=['POST'])
    def fs_remove_dir():
        params = request.json
        res = fs.delete_directory(params.get('directory', None))
        return jsonify(res)

    return router
