import os
import pathlib
import platform
import shutil
import subprocess


def open_directory(path):
    if path is None:
        return False

    pipe = None
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        pipe = subprocess.Popen(["open", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        pipe = subprocess.Popen(["xdg-open", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if pipe is not None:
        res, err = pipe.communicate()
        if len(err):
            raise Exception("Can't open directory")

    return True


def delete_directory(path):
    if not path:
        return False

    directory = pathlib.Path(path)
    if not directory.exists():
        return False

    if directory.is_dir():
        shutil.rmtree(path)
    elif directory.is_file():
        directory.unlink()

    return True


def create_directory(path):
    return pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def list_directory(path):
    return os.listdir(path)


def get_directory_tree(path, exclude=[]):
    for substr in exclude:
        if substr in path:
            return

    d = {
        'name': os.path.basename(path),
        'path': path
    }
    if os.path.isdir(path):
        d['type'] = "directory"
        d['tree'] = [get_directory_tree(os.path.join(path, x)) for x in os.listdir(path)]
        d['tree'] = [x for x in d['tree'] if x is not None]
    else:
        d['type'] = "file"
    return d
