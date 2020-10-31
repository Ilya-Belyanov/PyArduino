class PyArdAdapter:

    def __init__(self, port=None):
        self.port = port

    def do(self, command):
        if self.port:
            self.port.write(command)

    def readInt(self, sensor):
        return int(self.read(sensor))

    def readFloat(self, sensor):
        return float(self.read(sensor))

    def read(self, sensor):
        if self.port:
            self.port.write(sensor)
            res = self.port.readline()
            return res.decode('utf-8')
        return 0