import json


class Style:
    PURPLE = "static/style/style.css"
    BW = "static/style/styleBW.css"

    PATH_ST = "static/style/style.txt"

    def __init__(self, window):
        self.window = window
        self.window.loadStyleSheets(self.load())

    def setPurpleStyle(self):
        self.save(self.PURPLE)
        self.window.loadStyleSheets(self.load())

    def setBWStyle(self):
        self.save(self.BW)
        self.window.loadStyleSheets(self.load())

    @staticmethod
    def save(lg: str = None):
        with open(Style.PATH_ST, 'w') as f:
            json.dump(lg, f)

    @staticmethod
    def load():
        with open(Style.PATH_ST) as f:
            return json.load(f)