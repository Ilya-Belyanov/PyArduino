from src.obj.PyArduinoAdapter import PyArdAdapter
from data.command import Command


class Analyzer:
    DISTANCE = True
    LINE = True
    LIGHT = True
    TEMPERATURE = True

    def __init__(self, parent):
        self.parent = parent
        self.adapter = PyArdAdapter()

    def setPort(self, port):
        self.adapter.port = port
        self.adapter.do(Command.BEGIN)

    def boolDistance(self):
        self.DISTANCE = not self.DISTANCE
        return self.DISTANCE

    def boolLine(self):
        self.LINE = not self.LINE
        return self.LINE

    def boolLight(self):
        self.LIGHT = not self.LIGHT
        return self.LIGHT

    def boolTemperature(self):
        self.TEMPERATURE = not self.TEMPERATURE
        return self.TEMPERATURE

    def readDistance(self):
        if self.DISTANCE:
            self.parent.writeDistance(self.adapter.readInt(Command.DISTANT_SENSOR_READ))

    def readLine(self):
        if self.LINE:
            line = self.adapter.readInt(Command.LINE_SENSOR_READ)
            color = "LIGHT" if line < 800 else "BLACK"
            self.parent.writeLine(line, color)

    def readLight(self):
        if self.LIGHT:
            self.parent.writeLight(self.adapter.readInt(Command.LIGHT_SENSOR_READ))

    def readTemperature(self):
        if self.TEMPERATURE:
            self.parent.writeTemperature(self.adapter.readFloat(Command.TEMP_SENSOR_READ))