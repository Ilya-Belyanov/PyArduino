import json

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator, QCoreApplication

import static.qrc_generated.res


class Language:
    RU = ":/res/translate/eng-ru.qm"
    ENG = " "

    PATH_LG = "static/language/lg.txt"

    def __init__(self, window):
        self.window = window
        self.translator = QTranslator(window)
        self.translator.load(self.load())
        QtWidgets.QApplication.instance().installTranslator(self.translator)
        self.translate = QCoreApplication.translate

    def setRu(self):
        if self.load() != self.RU:
            self.save(self.RU)
            QtWidgets.QMessageBox.about(self.window, "Смена языка",
                                        "Перезагрузитесь для смены языка")

    def setEng(self):
        if self.load() != self.ENG:
            self.save(self.ENG)
            QtWidgets.QMessageBox.about(self.window, "Change language",
                                        "Reload for change language")

    @staticmethod
    def save(lg: str = None):
        with open(Language.PATH_LG, 'w') as f:
            json.dump(lg, f)

    @staticmethod
    def load():
        with open(Language.PATH_LG) as f:
            return json.load(f)

