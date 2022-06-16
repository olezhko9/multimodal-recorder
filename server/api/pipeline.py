import json
import os
import time
import traceback
import preprocess
import utils.flie_system as fs
import numpy as np

from flask import Blueprint, request, jsonify
from service import record_service
from preprocess import run_pipeline
from cv2 import cv2


def get_api():
    router = Blueprint('pipeline_router', __name__)

    @router.route('/pipeline/methods')
    def get_pipeline_methods():
        return jsonify(preprocess.get_allowed_scripts())

    @router.route('/pipeline/run', methods=['POST'])
    def pipeline_run():
        params = request.json
        record = record_service.get_record(record_id=params['record_id'])
        record_dir = record_service.get_record_dir(params['record_id'])
        modality = record['device_modality_dict'].get(params['device_id'], None)
        print(modality)

        data_path = params['data_path']
        loaded = preprocess.load_data(data_path, modality)
        if loaded is None:
            raise Exception("Can't load data")

        filenames, data, meta = loaded
        columns = []
        if modality.startswith('serial'):
            columns = list(data.columns)
            data = data.to_numpy().transpose()

        preprocess_data_path = record_dir + f"/{params['device_id']}_pipeline_{str(round(time.time() * 1000))}"
        fs.create_directory(preprocess_data_path)

        try:
            pipeline = params['pipeline']
            meta['pipeline'] = pipeline
            device = meta.get('device', {})

            data = run_pipeline(pipeline, data, device)

            if modality == "visual/image":
                for filename, image in zip(filenames, data):
                    cv2.imwrite(os.path.join(preprocess_data_path, filename), image)
            elif modality.startswith('serial'):
                with open(os.path.join(preprocess_data_path, filenames[0]), 'a') as f:
                    f.write(json.dumps(meta, default=str) + '\n')
                    f.write(','.join(columns) + '\n')
                    np.savetxt(f, X=np.transpose(data), delimiter=',', fmt='%f')
        except Exception:
            traceback.print_exc()
            raise Exception('Error while exec pipeline. Look server console for details')

        return jsonify(True)

    return router
