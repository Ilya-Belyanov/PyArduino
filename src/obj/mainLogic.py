from data.command import Command
from src.obj.analyzer import Analyzer
from src.obj.commander import Commander


class MainLogic:
    def __init__(self, window, ui=None):
        self.window = window
        self.ui = ui

        self.commander = Commander(self.window)
        self.analyzer = Analyzer(self)

    def setStartWindow(self):
        self.clearRGB()
        self.writeDistance()
        self.writeLine()
        self.writeLight()
        self.writeTemperature()
        self.ui.bLaser.setText(self.window.language.words.ON)
        self.commander.LASER = False

    def setStartWindowWithoutPort(self):
        self.setStartWindow()
        self.ui.bLaser.setEnabled(False)
        self.window.timeStop()

    def setStartWindowWithPort(self):
        self.setStartWindow()
        self.ui.bLaser.setEnabled(True)
        self.window.timeStart()

    def setPort(self, port):
        self.analyzer.setPort(port)
        self.commander.setPort(port)
        self.setStartWindowWithPort()

    def closePort(self):
        self.setStartWindowWithoutPort()
        self.commander.closePort()
        self.analyzer.adapter.closePort()

    def clearRGB(self):
        self.ui.sR.setValue(0)
        self.ui.sG.setValue(0)
        self.ui.sB.setValue(0)

    def changeColor(self, command, color):
        self.commander.changeColor(command, color)
        self.ui.lR.setText(str(self.ui.sR.value()))
        self.ui.lG.setText(str(self.ui.sG.value()))
        self.ui.lB.setText(str(self.ui.sB.value()))

    def checkLaser(self):
        self.commander.writeLaser()
        if self.commander.LASER:
            self.ui.bLaser.setText(self.window.language.words.OFF)
        else:
            self.ui.bLaser.setText(self.window.language.words.ON)

    def changeBool(self, command, setStart):
        self.analyzer.READ[command] = not self.analyzer.READ[command]
        if self.analyzer.READ[command]:
            self.window.sender().setText(self.window.language.words.OFF)
        else:
            self.window.sender().setText(self.window.language.words.ON)
        setStart()

    def writeDistance(self, distance: int = 0):
        self.ui.lcdDistance.display(distance)
        if not self.analyzer.READ[Command.DISTANT_SENSOR_READ]:
            self.commander.ledLow()

    def writeLine(self, var: int = 0, color: str = " "):
        self.ui.lcdLine.display(var)
        self.ui.lLine.setText(color)

    def writeLight(self, light: int = 0):
        self.ui.lcdLight.display(light)

    def writeTemperature(self, temp: float = 0.0):
        self.ui.lcdTemperature.display(temp)
