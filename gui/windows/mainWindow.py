import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QBasicTimer

from ..ui.ui_generated.MainWindow import Ui_MainWindow
from .portWindow import PortWindow
from data.parameters import FPS, FPS_TEMP
from src.obj.analyzer import Analyzer
from src.obj.commander import Commander
from data.command import Command


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.analyzer = Analyzer(self)
        self.commander = Commander(self)
        self.portWindow = PortWindow(self)

        self.ui.actionConnect_port.triggered.connect(self.showPortWindow)
        self.ui.bDistance.clicked.connect(lambda: self.changeBool(self.analyzer.boolDistance, self.writeDistance))
        self.ui.pushButton.clicked.connect(lambda: self.changeBool(self.analyzer.boolLine, self.writeLine))
        self.ui.pushButton_2.clicked.connect(lambda:
                                             self.changeBool(self.analyzer.boolTemperature, self.writeTemperature))
        self.ui.pushButton_4.clicked.connect(lambda: self.changeBool(self.analyzer.boolLight, self.writeLight))

        self.ui.pushButton_3.clicked.connect(self.setStartWindow)

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

    def loadStyleSheets(self):
        style = "static/style/style.css"
        with open(style, "r") as f:
            self.setStyleSheet(f.read())

    def changeBool(self, boolValue, setStart):
        if boolValue():
            self.sender().setText("Off")
        else:
            self.sender().setText("On")
        setStart()

    def setStartWindow(self):
        self.ui.sR.setValue(0)
        time.sleep(0.01)
        self.ui.sG.setValue(0)
        time.sleep(0.01)
        self.ui.sB.setValue(0)

    def showPortWindow(self):
        self.portWindow.show()

    def setPort(self, port):
        self.analyzer.setPort(port)
        self.commander.setPort(port)
        self.setStartWindow()

    def closeEvent(self, event):
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

    def changeColor(self, command, color):
        self.commander.changeColor(command, color)
        self.ui.lR.setText(str(self.ui.sR.value()))
        self.ui.lG.setText(str(self.ui.sG.value()))
        self.ui.lB.setText(str(self.ui.sB.value()))

    def writeDistance(self, distance: int = 0):
        self.ui.lcdNumber.display(distance)

    def writeLine(self, var: int = 0, color: str = " "):
        self.ui.lcdNumber_2.display(var)
        self.ui.label_2.setText(color)

    def writeLight(self, light: int = 0):
        self.ui.lcdNumber_4.display(light)

    def writeTemperature(self, temp: float = 0.0):
        self.ui.lcdNumber_3.display(temp)









