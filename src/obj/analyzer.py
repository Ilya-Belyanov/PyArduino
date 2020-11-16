from data.command import Command
from src.obj.PyArduinoAdapter import PyArdAdapter


class Analyzer:
    READ = {Command.DISTANT_SENSOR_READ: True,
            Command.LINE_SENSOR_READ: True,
            Command.LIGHT_SENSOR_READ: True,
            Command.TEMP_SENSOR_READ: True}

    def __init__(self, parent):
        self.parent = parent
        self.adapter = PyArdAdapter()

    def setPort(self, port):
        self.adapter.port = port
        self.adapter.do(Command.BEGIN)

    def readDistance(self):
        if self.READ[Command.DISTANT_SENSOR_READ]:
            distance = self.adapter.readInt(Command.DISTANT_SENSOR_READ)
            self.parent.writeDistance(distance)

    def readLine(self):
        if self.READ[Command.LINE_SENSOR_READ]:
            line = self.adapter.readInt(Command.LINE_SENSOR_READ)
            color = self.parent.language.words.LIGHT if line < 800 else self.parent.language.words.BLACK
            self.parent.writeLine(line, color)

    def readLight(self):
        if self.READ[Command.LIGHT_SENSOR_READ]:
            self.parent.writeLight(self.adapter.readInt(Command.LIGHT_SENSOR_READ))

    def readTemperature(self):
        if self.READ[Command.TEMP_SENSOR_READ]:
            self.parent.writeTemperature(self.adapter.readFloat(Command.TEMP_SENSOR_READ))