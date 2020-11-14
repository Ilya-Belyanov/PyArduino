import json


class Language:
    RU = 'ru'
    ENG = 'eng'

    words = None

    PATH = 'static/language/lg.txt'

    def __init__(self):
        if self.load() == self.RU:
            self.words = WordsRu()
        elif self.load() == self.ENG:
            self.words = WordsEng()
        else:
            self.words = WordsRu()

    def setRu(self):
        self.save(self.RU)

    def setEng(self):
        self.save(self.ENG)

    @staticmethod
    def save(lg: str = None):
        with open(Language.PATH, 'w') as f:
            json.dump(lg, f)

    @staticmethod
    def load():
        with open(Language.PATH) as f:
            return json.load(f)


class WordsEng:
    TITLE = "Title"

    ON = 'on'
    OFF = 'off'
    CLEAR = 'clear'

    SETTINGS = "Settings"
    CONNECT_PORT = "Connect port"
    LANGUAGE = "Language"
    RU = "Ru"
    ENG = "Eng"

    DISTANT_SENSOR = "Distant sensor"
    LINE_SENSOR = "Line sensor"
    LIGHT_SENSOR = "Light sensor"
    TEMP_SENSOR = "Temperature sensor"

    BLACK = "Black"
    LIGHT = "Light"

    LASER = "Laser"

    """Connect window"""
    CONNECT = "Connect"
    CANCEL = "Cancel"

    PORTS = "Choice available port"
    SPEEDS = "Choice speed of port"


class WordsRu:
    TITLE = "Название"

    ON = 'вкл'
    OFF = 'выкл'
    CLEAR = 'Погасить'

    SETTINGS = "Настройки"
    CONNECT_PORT = "Подключить порт"
    LANGUAGE = "Язык"
    RU = "Ру"
    ENG = "Инг"

    DISTANT_SENSOR = "Датчик дистанции"
    LINE_SENSOR = "Датчик линии"
    LIGHT_SENSOR = "Датчик света"
    TEMP_SENSOR = "Датчик температуры"

    BLACK = "Черный"
    LIGHT = "Белый"

    LASER = "Лазер"

    """Connect window"""
    CONNECT = "Подключить"
    CANCEL = "Отмена"

    PORTS = "Выберите порт"
    SPEEDS = "Выберите скорость"
