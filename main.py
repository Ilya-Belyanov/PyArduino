import sys
from PyQt5 import QtWidgets
import logging
from src.core.modules.ui_converter import ui_convert
from gui.windows.mainWindow import MainWindow


if __name__ == '__main__':
    ui_convert()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
