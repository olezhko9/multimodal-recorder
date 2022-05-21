from flask import Blueprint, request, jsonify
from os.path import isfile, join
from config import config
from notebook_manager import execute_notebook

import threading
import utils.flie_system as fs


def get_api():
    router = Blueprint('notebook_router', __name__)

    @router.route('/notebook', methods=["GET"])
    def get_notebooks():
        notebooks_dir = config.get('notebooks_dir', None)

        notebooks = [f for f in fs.list_directory(notebooks_dir) if
                     f.endswith('.ipynb') and isfile(join(notebooks_dir, f))]

        return jsonify(notebooks)

    @router.route('/notebook/run', methods=['POST'])
    def run_notebook():
        params = request.json
        notebook_name = params.get('notebook', None)
        record_id = params.get('record_id', None)

        notebooks_dir = config.get('notebooks_dir', None)
        notebook_path = join(notebooks_dir, notebook_name)
        # создаем папку для сгенерированного notebook
        notebook_out_dir = join(notebooks_dir, 'record_' + record_id)
        fs.create_directory(notebook_out_dir)

        notebook_out_path = f'{notebook_out_dir}/{notebook_name}'

        thread = threading.Thread(target=execute_notebook, kwargs={
            'notebook_filename': notebook_path,
            'notebook_filename_out': notebook_out_path,
            'params_dict': {
                'DATA_DIR': params.get('data_path', None)
            }
        })
        thread.start()

        return jsonify(notebook_out_dir)

    return router
