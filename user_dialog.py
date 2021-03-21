from enum import Enum

from vk_api.vk_api import VkApiMethod

from vk_user import VkUser


class Command(Enum):
    help = ["Помощь", 'help']
    gender = ["gender"]


class Mode(Enum):
    listen = ["Обычный режим"]
    get_answer = ["Режим ввода ответа"]


class Dialog:

    def __init__(self, vk_user: VkUser):
        self.user = vk_user
        self.mode = Mode.listen

    def _start_message(self):
        """

        :return:
        """
        return f"Привет {self.user}\n" \
               f"Твой возраст: {self.user.age}\n" \
               f"Твой пол: {self.user.sex}\n" \
               f"Твой город {self.user.city}"

    def _help_message(self):
        """

        :return:
        """
        return f"Добавить возраст. Пример: /age 20\n" \
               f"Добавить пол. Пример: /sex M\n" \
               f"Добавить город. Пример: /city Москва"

    def input(self, message):
        """
        Функция принимающая сообщения пользователя
        :param message: Сообщение
        :return: Ответ пользователю, отправившему сообщение
        """
        if self.mode == Mode.listen:
            if message.startswith("/"):
                for command in Command:
                    if message[1::] in command.value:
                        return "Help"
            return self._start_message()
