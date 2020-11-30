import time
import serial

from PyQt5 import QtWidgets

from gui.ui.ui_generated.portWindow import Ui_MainWindow
from src.core.modules.port import serial_ports
from data.parameters import AVAILABLE_SPEED
from data.parameters import TIME_CONNECT


class PortWindow(QtWidgets.QMainWindow):
    selectPort = None

    def __init__(self, window):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.window = window
        self.language = self.window.language
        self.ui.port.addItems(serial_ports())
        self.ui.speed.addItems(AVAILABLE_SPEED)
        self.ui.connect.clicked.connect(self.connect)
        self.ui.progressBar.setValue(0)
        self.ui.OK.clicked.connect(self.OK)
        self.ui.Cancel.clicked.connect(self.Cancel)
        self.ui.lConnect.setText("Not connected port")
        self.loadStyleSheets()

        self.ui.retranslateUi(self)

    def loadStyleSheets(self):
        style = self.window.st.load()
        with open(style, "r") as f:
            self.setStyleSheet(f.read())

    def connect(self):
        try:
            self.selectPort = serial.Serial(self.ui.port.currentText(), int(self.ui.speed.currentText()))
            self.runBar()
            self.ui.lConnect.setText("Success connect")
        except Exception as e:
            self.ui.lConnect.setScaledContents(True)
            self.ui.lConnect.setWordWrap(True)
            self.ui.lConnect.setText(str(e))

    def runBar(self):
        self.ui.OK.setEnabled(False)
        for i in range(100):
            self.ui.progressBar.setValue(i + 1)
            time.sleep(TIME_CONNECT/100)
        self.ui.OK.setEnabled(True)

    def OK(self):
        if self.selectPort:
            self.window.logic.setPort(self.selectPort)
        self.close()

    def Cancel(self):
        if self.selectPort:
            self.selectPort.close()
        self.close()
