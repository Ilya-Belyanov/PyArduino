import os
import subprocess


def ui_convert():
    path = os.getcwd()
    converter = "static/scripts/ui_converter.bat"
    args = [converter, "gui/ui", "gui/ui/ui_generated"]
    subprocess.call([os.path.join(path, arg) for arg in args])