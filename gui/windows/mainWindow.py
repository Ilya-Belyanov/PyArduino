from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QBasicTimer
from PyQt5 import QtWidgets

from data.command import Command
from .portWindow import PortWindow
from src.obj.mainLogic import MainLogic
from data.parameters import FPS, FPS_TEMP
from static.language.language import Language
from static.style.style import Style
from ..ui.ui_generated.MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.portWindow = None
        self.language = Language(self)
        self.st = Style(self)
        self.logic = MainLogic(self)

        self.ui.actionConnect_port.triggered.connect(self.showPortWindow)
        self.ui.actionRu_2.triggered.connect(self.language.setRu)
        self.ui.actionEng.triggered.connect(self.language.setEng)
        self.ui.actionPurple.triggered.connect(self.st.setPurpleStyle)
        self.ui.actionBW.triggered.connect(self.st.setBWStyle)
        self.ui.actionClose_port.triggered.connect(self.logic.closePort)
        self.ui.actionParameters_port.triggered.connect(lambda:
                                                        QMessageBox.about(self, "Parameters of port",
                                                                          self.logic.parametersPort()))

        self.ui.bDistance.clicked.connect(lambda:
                                          self.logic.changeBool(Command.DISTANT_SENSOR_READ, self.logic.clearDistance))
        self.ui.bLine.clicked.connect(lambda: self.logic.changeBool(Command.LINE_SENSOR_READ, self.logic.writeLine))
        self.ui.bTemperature.clicked.connect(lambda:
                                             self.logic.changeBool(Command.TEMP_SENSOR_READ,
                                                                   self.logic.writeTemperature))
        self.ui.bLight.clicked.connect(lambda: self.logic.changeBool(Command.LIGHT_SENSOR_READ, self.logic.writeLight))

        self.ui.bLaser.clicked.connect(self.logic.checkLaser)
        self.ui.bClear.clicked.connect(self.logic.clearRGB)

        self.ui.sR.setRange(0, 255)
        self.ui.sR.valueChanged[int].connect(lambda r: self.logic.changeColor(Command.R, r))
        self.ui.sG.setRange(0, 255)
        self.ui.sG.valueChanged[int].connect(lambda g: self.logic.changeColor(Command.G, g))
        self.ui.sB.setRange(0, 255)
        self.ui.sB.valueChanged[int].connect(lambda b: self.logic.changeColor(Command.B, b))

        self.ui.retranslateUi(self)

        self.groupAction()

        self.timer = QBasicTimer()
        self.timerTemp = QBasicTimer()
        self.timeStart()

        self.logic.setStartWindowWithoutPort()

    def loadStyleSheets(self, style):
        with open(style, "r") as f:
            self.setStyleSheet(f.read())
        if self.portWindow:
            self.portWindow.loadStyleSheets()

    def groupAction(self):
        self.ui.actionEng.setCheckable(True)
        self.ui.actionRu_2.setCheckable(True)
        self.ui.actionRu_2.setChecked(self.language.load() == self.language.RU)
        self.ui.actionEng.setChecked(self.language.load() == self.language.ENG)
        self.actionGroup = QtWidgets.QActionGroup(self)
        self.actionGroup.addAction(self.ui.actionEng)
        self.actionGroup.addAction(self.ui.actionRu_2)

        self.ui.actionPurple.setCheckable(True)
        self.ui.actionPurple.setChecked(self.st.load() == self.st.PURPLE)
        self.ui.actionBW.setCheckable(True)
        self.ui.actionBW.setChecked(self.st.load() == self.st.BW)
        self.actionGroup2 = QtWidgets.QActionGroup(self)
        self.actionGroup2.addAction(self.ui.actionPurple)
        self.actionGroup2.addAction(self.ui.actionBW)

    def showPortWindow(self):
        self.portWindow = PortWindow(self)
        self.portWindow.show()

    def closeEvent(self, event):
        self.logic.closePort()
        if self.portWindow:
            self.portWindow.close()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.logic.reader.readDistance()
            self.logic.reader.readLine()
            self.logic.reader.readLight()

        if event.timerId() == self.timerTemp.timerId():
            self.logic.reader.readTemperature()

    def timeStop(self):
        self.timer.stop()
        self.timerTemp.stop()

    def timeStart(self):
        self.timer.start(int(1000 / FPS), self)
        self.timerTemp.start(int(1000 / FPS_TEMP), self)
