import sys
from PyQt5 import QtWidgets, QtGui
import logging
from src.core.modules.scripts import convert
from gui.windows.mainWindow import MainWindow


if __name__ == '__main__':
    convert()
    app = QtWidgets.QApplication(sys.argv)
    img = QtGui.QPixmap('static\img\экран.png')
    splash = QtWidgets.QSplashScreen(img)
    splash.show()
    window = MainWindow()
    splash.finish(window)
    window.show()
    app.exec_()
