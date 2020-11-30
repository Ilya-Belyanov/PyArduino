import time

from src.obj.PyArduinoAdapter import PyArdAdapter
from data.command import Command


def timeFreeze(func):
    def wrapper(cls, *args):
        if cls.adapter.port:
            cls.window.timeStop()
            func(cls, *args)
            time.sleep(0.001)
            cls.window.timeStart()

    return wrapper


class Commander:
    RGB = {Command.R: 0, Command.G: 0, Command.B: 0}
    LASER = False
    LED_DISTANCE = False

    def __init__(self, window=None):
        self.window = window
        self.adapter = PyArdAdapter()

    def setPort(self, port):
        self.adapter.port = port

    def closePort(self):
        self.adapter.do(Command.END)
        self.adapter.closePort()

    def reload(self):
        self.LASER = False
        self.LED_DISTANCE = False

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

    def ledLow(self):
        self.adapter.do(Command.LED_LOW)

    def ledHigh(self):
        self.adapter.do(Command.LED_HIGH)



