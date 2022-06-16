import pandas as pd
import importlib
import json
import pkgutil
import os

from cv2 import cv2
from config import config


def get_module(module_name):
    try:
        return importlib.import_module(config.get('scripts_dir')[2:] + '.' + module_name)
    except ModuleNotFoundError:
        return None


def get_allowed_scripts():
    scripts = [name for _, name, _ in pkgutil.iter_modules([config.get('scripts_dir')])]
    allowed_methods = []
    for script in scripts:
        module = get_module(script)
        if module is None:
            continue

        script_config = {}
        if hasattr(module, 'get_config') and callable(getattr(module, 'get_config')):
            script_config = module.get_config()

        script_dict = {'name': script}
        script_dict = {**script_dict, **script_config}
        allowed_methods.append(script_dict)

    return allowed_methods


def read_multimodal(path):
    meta = None
    data = []
    columns = []
    f = open(path)
    line_i = 0
    while True:
        line = f.readline().strip()
        if not line:
            break

        if line_i == 0:
            meta = json.loads(line)
        elif line_i == 1:
            columns = line.split(',')
        else:
            data.append(map(float, line.split(',')))
        line_i += 1

    return meta, pd.DataFrame(data, columns=columns)


def load_data(data_path, modality):
    if modality == 'visual/image':
        images = []
        filenames = [filename for filename in os.listdir(data_path)]
        for filename in filenames:
            img = cv2.imread(os.path.join(data_path, filename))
            if img is not None:
                images.append(img)

        return filenames, images, {}

    if modality.startswith('serial'):
        filenames = [filename for filename in os.listdir(data_path) if filename.endswith('txt')]
        filename = filenames[0]
        if filename:
            meta, data = read_multimodal(os.path.join(data_path, filename))

            return [filename], data, meta

    return None


def run_script(script_name, data, options, device):
    module = get_module(script_name)
    if module is None:
        return False

    if hasattr(module, 'run') and callable(getattr(module, 'run')):
        return module.run(data, options, device)


def run_pipeline(pipeline, data, device):
    for script in pipeline:
        data = run_script(script['name'], data, script['options'], device)

    return data
