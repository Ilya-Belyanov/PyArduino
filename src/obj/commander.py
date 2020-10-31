from src.obj.PyArduinoAdapter import PyArdAdapter
from data.command import Command


class Commander:
    RGB = [0, 0, 0]

    def __init__(self, parent):
        self.parent = parent
        self.adapter = PyArdAdapter()

    def setPort(self, port):
        self.adapter.port = port

    def changeR(self, r):
        self.parent.timeStop()
        self.RGB[0] = r
        command = Command.R + str(self.RGB[0])
        self.adapter.do(bytes(command, 'utf-8'))
        self.parent.timeStart()

    def changeG(self, g):
        self.parent.timeStop()
        self.RGB[1] = g
        command = Command.G + str(self.RGB[1])
        self.adapter.do(bytes(command, 'utf-8'))
        self.parent.timeStart()

    def changeB(self, b):
        self.parent.timeStop()
        self.RGB[2] = b
        command = Command.B + str(self.RGB[2])
        self.adapter.do(bytes(command, 'utf-8'))
        self.parent.timeStart()