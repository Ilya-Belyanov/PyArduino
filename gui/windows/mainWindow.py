import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QBasicTimer

from ..ui.ui_generated.MainWindow import Ui_MainWindow
from .portWindow import PortWindow
from src.obj.analyzer import Analyzer
from src.obj.commander import Commander
from data.parameters import FPS, FPS_TEMP
from data.command import Command
from static.language.language import Language


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.language = Language()

        self.analyzer = Analyzer(self)
        self.commander = Commander(self)

        self.portWindow = None

        self.ui.actionConnect_port.triggered.connect(self.showPortWindow)
        self.ui.actionRu_2.triggered.connect(self.language.setRu)
        self.ui.actionEng.triggered.connect(self.language.setEng)

        self.ui.bDistance.clicked.connect(lambda: self.changeBool(Command.DISTANT_SENSOR_READ, self.writeDistance))
        self.ui.bLine.clicked.connect(lambda: self.changeBool(Command.LINE_SENSOR_READ, self.writeLine))
        self.ui.bTemperature.clicked.connect(lambda:
                                             self.changeBool(Command.TEMP_SENSOR_READ, self.writeTemperature))
        self.ui.bLight.clicked.connect(lambda: self.changeBool(Command.LIGHT_SENSOR_READ, self.writeLight))

        self.ui.bLaser.clicked.connect(self.checkLaser)
        self.ui.bClear.clicked.connect(self.clearRGB)

        self.ui.sR.setRange(0, 255)
        self.ui.sR.valueChanged[int].connect(lambda r: self.changeColor(Command.R, r))
        self.ui.sG.setRange(0, 255)
        self.ui.sG.valueChanged[int].connect(lambda g: self.changeColor(Command.G, g))
        self.ui.sB.setRange(0, 255)
        self.ui.sB.valueChanged[int].connect(lambda b: self.changeColor(Command.B, b))

        self.timer = QBasicTimer()
        self.timerTemp = QBasicTimer()
        self.timeStart()

        self.loadStyleSheets()
        self.setLanguage()
        self.setStartWindow()

    def loadStyleSheets(self):
        style = "static/style/style.css"
        with open(style, "r") as f:
            self.setStyleSheet(f.read())

    def setLanguage(self):
        self.setWindowTitle(self.language.words.TITLE)

        self.ui.menuSettings.setTitle(self.language.words.SETTINGS)
        self.ui.actionConnect_port.setText(self.language.words.CONNECT_PORT)
        self.ui.menuLanguages.setTitle(self.language.words.LANGUAGE)
        self.ui.actionRu_2.setText(self.language.words.RU)
        self.ui.actionEng.setText(self.language.words.ENG)

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
        self.ui.bLaser.setText(self.language.words.ON)

    def setStartWindow(self):
        self.clearRGB()
        self.ui.bLaser.setEnabled(False)

    def clearRGB(self):
        self.ui.sR.setValue(0)
        time.sleep(0.01)
        self.ui.sG.setValue(0)
        time.sleep(0.01)
        self.ui.sB.setValue(0)

    def showPortWindow(self):
        self.portWindow = PortWindow(self)
        self.portWindow.show()

    def setPort(self, port):
        self.analyzer.setPort(port)
        self.commander.setPort(port)
        self.setStartWindow()
        self.ui.bLaser.setEnabled(True)

    def closeEvent(self, event):
        self.analyzer.adapter.closePort()
        self.commander.adapter.closePort()

        if self.portWindow:
            self.portWindow.close()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.analyzer.readDistance()
            self.analyzer.readLine()
            self.analyzer.readLight()

        if event.timerId() == self.timerTemp.timerId():
            self.analyzer.readTemperature()

    def timeStop(self):
        self.timer.stop()
        self.timerTemp.stop()

    def timeStart(self):
        self.timer.start(int(1000 / FPS), self)
        self.timerTemp.start(int(1000 / FPS_TEMP), self)

    def checkLaser(self):
        self.commander.writeLaser()
        if self.commander.LASER:
            self.sender().setText(self.language.words.OFF)
        else:
            self.sender().setText(self.language.words.ON)

    def changeColor(self, command, color):
        self.commander.changeColor(command, color)
        self.ui.lR.setText(str(self.ui.sR.value()))
        self.ui.lG.setText(str(self.ui.sG.value()))
        self.ui.lB.setText(str(self.ui.sB.value()))

    def changeBool(self, command, setStart):
        self.analyzer.READ[command] = not self.analyzer.READ[command]
        if self.analyzer.READ[command]:
            self.sender().setText(self.language.words.OFF)
        else:
            self.sender().setText(self.language.words.ON)
        setStart()

    def writeDistance(self, distance: int = 0):
        self.ui.lcdDistance.display(distance)

    def writeLine(self, var: int = 0, color: str = " "):
        self.ui.lcdLine.display(var)
        self.ui.lLine.setText(color)

    def writeLight(self, light: int = 0):
        self.ui.lcdLight.display(light)

    def writeTemperature(self, temp: float = 0.0):
        self.ui.lcdTemperature.display(temp)









