from enum import Enum

from vk_api.vk_api import VkApiMethod

from vk_user import VkUser


class Command(Enum):
    bdate = ["bdate"]
    gender = ["gender"]


class Mode(Enum):
    default = ["Обычный режим", "default"]
    get_answer = ["Режим ввода ответа"]


class Dialog:

    def __init__(self, vk_user: VkUser):
        user = vk_user

    def input(self, message):
        """
        Функция принимающая сообщения пользователя
        :param message: Сообщение
        :return: Ответ пользователю, отправившему сообщение
        """
        pass