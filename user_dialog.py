from enum import Enum


class Command(Enum):
    bdate = ["bdate"]
    gender = ["gender"]


class Mode(Enum):
    default = ["Обычный режим", "default"]
    get_answer = ["Режим ввода ответа"]