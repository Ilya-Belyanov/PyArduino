from PyQt5 import QtWidgets
from PyQt5.QtCore import QBasicTimer

from ..ui.ui_generated.MainWindow import Ui_MainWindow
from .portWindow import PortWindow
from data.parameters import FPS, FPS_TEMP
from src.obj.analyzer import Analyzer
from src.obj.commander import Commander


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.analyzer = Analyzer(self)
        self.commander = Commander(self)
        self.portWindow = PortWindow(self)

        self.ui.actionConnect_port.triggered.connect(self.showPortWindow)
        self.ui.bDistance.clicked.connect(self.analyzer.boolDistance)
        self.ui.pushButton.clicked.connect(self.analyzer.boolLine)
        self.ui.pushButton_2.clicked.connect(self.analyzer.boolTemp)

        self.ui.sR.setRange(0, 255)
        self.ui.sR.valueChanged[int].connect(lambda r: self.commander.changeR(r))
        self.ui.sG.setRange(0, 255)
        self.ui.sG.valueChanged[int].connect(lambda g: self.commander.changeG(g))
        self.ui.sB.setRange(0, 255)
        self.ui.sB.valueChanged[int].connect(lambda b: self.commander.changeB(b))

        self.timer = QBasicTimer()
        self.timerTemp = QBasicTimer()
        self.timeStart()

    def showPortWindow(self):
        self.portWindow.show()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.analyzer.readDistance()
            self.analyzer.readLine()

        if event.timerId() == self.timerTemp.timerId():
            self.analyzer.readTemperature()

    def timeStop(self):
        self.timer.stop()
        self.timerTemp.stop()

    def timeStart(self):
        self.timer.start(int(1000 / FPS), self)
        self.timerTemp.start(int(1000 / FPS_TEMP), self)

    def writeDistance(self, distance: int):
        self.ui.lcdNumber.display(distance)

    def writeLine(self, var: int, color: str):
        self.ui.lcdNumber_2.display(var)
        self.ui.label_2.setText(color)

    def writeTemperature(self, noise):
        self.ui.lcdNumber_3.display(noise)









