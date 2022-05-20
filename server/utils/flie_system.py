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
    directory = pathlib.Path(path)
    if not directory.exists():
        return False

    shutil.rmtree(path)
    return True


def create_directory(path):
    return pathlib.Path(path).mkdir(parents=True, exist_ok=True)
