from data.command import Command
from src.obj.reader import Reader
from src.obj.commander import Commander


class MainLogic:

    def __init__(self, window):
        self.window = window
        self.ui = window.ui
        self.language = window.language
        self.commander = Commander(self.window)
        self.reader = Reader(self, self.window)

    def setStartWindow(self):
        self.clearRGB()
        self.clearDistance()
        self.writeLine()
        self.writeLight()
        self.writeTemperature()
        self.ui.bLaser.setText(self.language.translate(self.window.objectName(), "On"))
        self.commander.reload()

    def setStartWindowWithoutPort(self):
        self.window.timeStop()
        self.setStartWindow()
        self.ui.bLaser.setEnabled(False)

    def setStartWindowWithPort(self):
        self.setStartWindow()
        self.ui.bLaser.setEnabled(True)
        self.window.timeStart()

    def setPort(self, port):
        self.reader.setPort(port)
        self.commander.setPort(port)
        self.setStartWindowWithPort()

    def closePort(self):
        self.setStartWindowWithoutPort()
        self.commander.closePort()
        self.reader.adapter.closePort()

    def parametersPort(self):
        dictParameters = self.reader.adapter.parameters()
        listP = ''
        for key in dictParameters.keys():
            listP += '{}: {}\n'.format(key, dictParameters[key])
        return listP

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
            self.ui.bLaser.setText(self.language.translate(self.window.objectName(), "Off"))
        else:
            self.ui.bLaser.setText(self.language.translate(self.window.objectName(), "On"))

    def changeBool(self, command, setStart):
        self.reader.READ[command] = not self.reader.READ[command]
        if self.reader.READ[command]:
            self.window.sender().setText(self.language.translate(self.window.objectName(), "Off"))
        else:
            self.window.sender().setText(self.language.translate(self.window.objectName(), "On"))
        setStart()

    def writeDistance(self, distance: int = 0):
        self.ui.lcdDistance.display(distance)
        self.analyzeDistance(distance)

    def clearDistance(self):
        self.ui.lcdDistance.display(0)
        self.commander.ledLow()
        self.commander.LED_DISTANCE = False

    def analyzeDistance(self, distance):
        if distance > 10 and self.commander.LED_DISTANCE:
            self.commander.ledLow()
            self.commander.LED_DISTANCE = False
        elif distance < 10 and not self.commander.LED_DISTANCE:
            self.commander.ledHigh()
            self.commander.LED_DISTANCE = True

    def writeLine(self, var: int = 0, color: str = " "):
        self.ui.lcdLine.display(var)
        self.ui.lLine.setText(color)

    def writeLight(self, light: int = 0):
        self.ui.lcdLight.display(light)

    def writeTemperature(self, temp: float = 0.0):
        self.ui.lcdTemperature.display(temp)
