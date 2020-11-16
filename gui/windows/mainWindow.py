from PyQt5 import QtWidgets
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QMessageBox

from data.command import Command
from .portWindow import PortWindow
from src.obj.mainLogic import MainLogic
from data.parameters import FPS, FPS_TEMP
from static.language.language import Language
from ..ui.ui_generated.MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.logic = MainLogic(self, self.ui)

        self.language = Language()
        self.portWindow = None

        self.ui.actionConnect_port.triggered.connect(self.showPortWindow)
        self.ui.actionRu_2.triggered.connect(self.language.setRu)
        self.ui.actionEng.triggered.connect(self.language.setEng)
        self.ui.actionClose_port.triggered.connect(self.logic.closePort)
        self.ui.actionParameters_port.triggered.connect(lambda: QMessageBox.about(self, "Title", "Message"))

        self.ui.bDistance.clicked.connect(lambda: self.logic.changeBool(Command.DISTANT_SENSOR_READ, self.writeDistance))
        self.ui.bLine.clicked.connect(lambda: self.logic.changeBool(Command.LINE_SENSOR_READ, self.writeLine))
        self.ui.bTemperature.clicked.connect(lambda:
                                             self.logic.changeBool(Command.TEMP_SENSOR_READ, self.writeTemperature))
        self.ui.bLight.clicked.connect(lambda: self.logic.changeBool(Command.LIGHT_SENSOR_READ, self.writeLight))

        self.ui.bLaser.clicked.connect(self.logic.checkLaser)
        self.ui.bClear.clicked.connect(self.logic.clearRGB)

        self.ui.sR.setRange(0, 255)
        self.ui.sR.valueChanged[int].connect(lambda r: self.logic.changeColor(Command.R, r))
        self.ui.sG.setRange(0, 255)
        self.ui.sG.valueChanged[int].connect(lambda g: self.logic.changeColor(Command.G, g))
        self.ui.sB.setRange(0, 255)
        self.ui.sB.valueChanged[int].connect(lambda b: self.logic.changeColor(Command.B, b))

        self.timer = QBasicTimer()
        self.timerTemp = QBasicTimer()
        self.timeStart()

        self.loadStyleSheets()
        self.setLanguage()

        self.logic.setStartWindowWithoutPort()

    def loadStyleSheets(self):
        style = "static/style/style.css"
        with open(style, "r") as f:
            self.setStyleSheet(f.read())

    def setLanguage(self):
        self.setWindowTitle(self.language.words.TITLE)

        self.ui.menuPort.setTitle(self.language.words.PORT)
        self.ui.actionParameters_port.setText(self.language.words.PARAMETERS_PORT)
        self.ui.actionConnect_port.setText(self.language.words.CONNECT_PORT)
        self.ui.actionClose_port.setText(self.language.words.CLOSE_PORT)

        self.ui.menuSettings.setTitle(self.language.words.SETTINGS)
        self.ui.menuLanguages.setTitle(self.language.words.LANGUAGE)
        self.ui.actionRu_2.setText(self.language.words.RU)
        self.ui.actionEng.setText(self.language.words.ENG)
        self.ui.actionStyles.setText(self.language.words.STYLES)

        self.ui.bDistance.setText(self.language.words.OFF)
        self.ui.groupBox.setTitle(self.language.words.DISTANT_SENSOR)

        self.ui.bLine.setText(self.language.words.OFF)
        self.ui.groupBox_2.setTitle(self.language.words.LINE_SENSOR)

        self.ui.bTemperature.setText(self.language.words.OFF)
        self.ui.groupBox_3.setTitle(self.language.words.TEMP_SENSOR)

        self.ui.bLight.setText(self.language.words.OFF)
        self.ui.groupBox_5.setTitle(self.language.words.LIGHT_SENSOR)

        self.ui.bClear.setText(self.language.words.CLEAR)

        self.ui.groupBox_6.setTitle(self.language.words.LASER)

    def showPortWindow(self):
        self.portWindow = PortWindow(self)
        self.portWindow.show()

    def closeEvent(self, event):
        self.logic.closePort()
        if self.portWindow:
            self.portWindow.close()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.logic.analyzer.readDistance()
            self.logic.analyzer.readLine()
            self.logic.analyzer.readLight()

        if event.timerId() == self.timerTemp.timerId():
            self.logic.analyzer.readTemperature()

    def timeStop(self):
        self.timer.stop()
        self.timerTemp.stop()

    def timeStart(self):
        self.timer.start(int(1000 / FPS), self)
        self.timerTemp.start(int(1000 / FPS_TEMP), self)
