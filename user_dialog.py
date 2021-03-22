from enum import Enum

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.vk_api import VkApiMethod

from vk_user import VkUser


class Command(Enum):
    help = ["Помощь", 'help']
    gender = ["gender"]


class Mode(Enum):
    listen = ["Обычный режим"]
    get_answer = ["Режим ввода ответа"]
    parse_age = False


class Dialog:

    def __init__(self, vk_user: VkUser):
        self.user = vk_user

        self.parse_age = False
        self.parse_city = False
        self.parse_sex = False

        # Стартовая клавиатура
        self.start_keyboard = VkKeyboard(one_time=False)
        self.start_keyboard.add_button('Найти', color=VkKeyboardColor.POSITIVE)
        self.start_keyboard.add_button('Настройки', color=VkKeyboardColor.SECONDARY)

        # Настройки клавиатура
        self.settings_keyboard = VkKeyboard(one_time=False)
        self.settings_keyboard.add_button('Возраст', color=VkKeyboardColor.POSITIVE)
        self.settings_keyboard.add_button('Город', color=VkKeyboardColor.POSITIVE)
        self.settings_keyboard.add_button('Пол', color=VkKeyboardColor.POSITIVE)
        self.settings_keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)

    def _start_keyboard(self):
        self.keyboard = VkKeyboard(one_time=False, inline=False)
        self.keyboard.add_callback_button(
            label="Настройки",
            color=VkKeyboardColor.PRIMARY,
            payload={"type": "settings"},
        )

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

    def input(self, message: str):
        """
        Функция принимающая сообщения пользователя
        :param message: Сообщение
        :return: Ответ пользователю, отправившему сообщение
        """
        if message.lower() == 'настройки':
            return {'message': 'Ваши критерии поиска', 'keyboard': self.settings_keyboard}

        if message.lower() == 'назад':
            return {'message': 'Готовы искать?', 'keyboard': self.start_keyboard}

        if message.lower() == 'возраст':
            self.parse_age = True
            return {'message': 'Введите возраст', 'keyboard': self.settings_keyboard}

        if message.lower() == 'город':
            self.parse_city = True
            return {'message': 'Введите город', 'keyboard': self.settings_keyboard}

        if message.lower() == 'пол':
            self.parse_sex = True
            return {'message': 'Введите пол', 'keyboard': self.settings_keyboard}

        if self.parse_age:
            # parse age and user.age = age
            self.parse_age = False
            return {'message': 'Ваш возраст', 'keyboard': self.settings_keyboard}

        if self.parse_city:
            # parse city and user.city = city
            self.parse_city = False
            return {'message': 'Ваш город', 'keyboard': self.settings_keyboard}

        if self.parse_sex:
            # parse sex and user.sex = sex
            self.parse_sex = False
            return {'message': 'Ваш пол', 'keyboard': self.settings_keyboard}

        return {'message': 'Привет', 'keyboard': self.start_keyboard}
