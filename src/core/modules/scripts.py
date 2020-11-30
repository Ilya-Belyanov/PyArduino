import os
import subprocess


def convert():
    ui_convert()
    qrc_convert()


def ui_convert():
    path = os.getcwd()
    converter = "static/scripts/ui_converter.bat"
    args = [converter, "gui/ui", "gui/ui/ui_generated"]
    subprocess.call([os.path.join(path, arg) for arg in args])


def qrc_convert():
    path = os.getcwd()
    converter = "static/scripts/qrc_converter.bat"
    args = [converter, "static", "static/qrc_generated"]
    subprocess.call([os.path.join(path, arg) for arg in args])
