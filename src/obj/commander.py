import time

from src.obj.PyArduinoAdapter import PyArdAdapter
from data.command import Command


def timeFreeze(func):
    def wrapper(cls, *args):
        if cls.adapter.port:
            cls.parent.timeStop()
            func(cls, *args)
            time.sleep(0.001)
            cls.parent.timeStart()

    return wrapper


class Commander:
    RGB = {Command.R: 0, Command.G: 0, Command.B: 0}
    LASER = None

    def __init__(self, parent=None):
        self.parent = parent
        self.adapter = PyArdAdapter()

    def setPort(self, port):
        self.adapter.port = port

    def closePort(self):
        self.adapter.do(Command.END)
        self.adapter.closePort()

    @timeFreeze
    def changeColor(self, color, count):
        self.RGB[color] = count
        command = color + str(self.RGB[color])
        self.adapter.do(bytes(command, 'utf-8'))

    @timeFreeze
    def writeLaser(self):
        if self.LASER:
            self.adapter.do(Command.LASER_LOW)
        else:
            self.adapter.do(Command.LASER_HIGH)
        self.LASER = not self.LASER

    @timeFreeze
    def ledLow(self):
        self.adapter.do(Command.LED_LOW)



