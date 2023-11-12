import logging
import os
import shutil
import subprocess
import sys


def get_platform():
    if sys.platform == "linux":
        try:
            proc_version = open("/proc/version").read()
            if "Microsoft" in proc_version:
                return "wsl"
        except:
            pass
    return sys.platform


def open_with_default_app(filename):
    platform = get_platform()
    file_name, file_extension = os.path.splitext(filename)
    temp_filename = file_name + "_copy" + file_extension

    if platform == "darwin":
        shutil.copy(filename, temp_filename)
        subprocess.call(("open", temp_filename))
    elif platform in ["win64", "win32"]:
        shutil.copyfile(filename, temp_filename)
        os.startfile(temp_filename.replace("/", "\\"))
    elif platform == "wsl":
        shutil.copy2(filename, temp_filename)
        subprocess.call("cmd.exe /C start".split() + [temp_filename])
    else:  # linux variants
        shutil.copyfile(filename, temp_filename)
        subprocess.call(("xdg-open", temp_filename))

    # Add a line to the copied file
    with open(temp_filename, "r+") as file:
        content = file.read()
        file.seek(0, 0)
        file.write(
            "This is a copy. Modifying this file won't change the data\n" + content
        )
