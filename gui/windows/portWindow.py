import time
import serial

from PyQt5 import QtWidgets

from gui.ui.ui_generated.portWindow import Ui_MainWindow
from src.core.modules.port import serial_ports
from data.parameters import AVAILABLE_SPEED


class PortWindow(QtWidgets.QMainWindow):
    selectPort = None

    def __init__(self, parent):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.port.addItems(serial_ports())
        self.ui.speed.addItems(AVAILABLE_SPEED)
        self.ui.connect.clicked.connect(self.connect)
        self.ui.progressBar.setValue(0)
        self.ui.OK.clicked.connect(self.OK)
        self.ui.Cancel.clicked.connect(lambda: self.close())
        self.loadStyleSheets()
        self.setLanguage()

    def loadStyleSheets(self):
        style = "static/style/style.css"
        with open(style, "r") as f:
            self.setStyleSheet(f.read())

    def setLanguage(self):
        self.ui.connect.setText(self.parent.language.words.CONNECT)
        self.ui.Cancel.setText(self.parent.language.words.CANCEL)
        self.ui.lPort.setText(self.parent.language.words.PORTS)
        self.ui.lSpeed.setText(self.parent.language.words.SPEEDS)

    def connect(self):
        try:
            self.selectPort = serial.Serial(self.ui.port.currentText(), int(self.ui.speed.currentText()))
            self.runBar()
            self.ui.connect.setStyleSheet("background-color: green")
        except Exception as e:
            print(e)

    def runBar(self):
        for i in range(100):
            self.ui.progressBar.setValue(i + 1)
            time.sleep(1/100)

    def OK(self):
        if self.selectPort:
            self.parent.setPort(self.selectPort)
        self.close()
