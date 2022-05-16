import os
import platform
import subprocess


def open_directory(path):
    if path is None:
        return False

    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

    return True
