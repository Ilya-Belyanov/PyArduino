from src.obj.PyArduinoAdapter import PyArdAdapter
from data.command import Command


def timeFreeze(func):
    def wrapper(cls, *args):
        cls.parent.timeStop()
        func(cls, *args)
        cls.parent.timeStart()

    return wrapper


class Commander:
    RGB = {Command.R: 0, Command.G: 0, Command.B: 0}

    def __init__(self, parent):
        self.parent = parent
        self.adapter = PyArdAdapter()

    def setPort(self, port):
        self.adapter.port = port

    @timeFreeze
    def changeColor(self, color, count):
        self.RGB[color] = count
        command = color + str(self.RGB[color])
        self.adapter.do(bytes(command, 'utf-8'))

