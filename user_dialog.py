import re
from enum import Enum

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.vk_api import VkApiMethod

from vk_user import VkUser

# todo Что лучше функция или класс?
class DialogAnswer:
    def __init__(self, message: str, keyboard: VkKeyboard):
        self.message = message
        self.keyboard = keyboard


class Command:
    def __init__(self, answer: DialogAnswer, action=None, await_answer: bool = False):
        self.answer = answer
        self.action = action
        self.await_answer = await_answer


class Dialog:

    def __init__(self, vk_user: VkUser, vk_api):
        self.user = vk_user
        self.vk_api = vk_api
        self.handler = None

        # todo Клавиатуры долыжны прекреплятся вне класса
        # Стартовая клавиатура
        self.start_keyboard = VkKeyboard(one_time=False)
        self.start_keyboard.add_button('Найти', color=VkKeyboardColor.POSITIVE)
        self.start_keyboard.add_button('Настройки', color=VkKeyboardColor.SECONDARY)

        # Преветсвие на непонятные сообщение
        self.current_answer = DialogAnswer(message='Привет', keyboard=self.start_keyboard)

        # Настройки клавиатура
        self.settings_keyboard = VkKeyboard(one_time=False)
        self.settings_keyboard.add_button('Возраст', color=VkKeyboardColor.POSITIVE)
        self.settings_keyboard.add_button('Город', color=VkKeyboardColor.POSITIVE)
        self.settings_keyboard.add_button('Пол', color=VkKeyboardColor.POSITIVE)
        self.settings_keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)

        self.commands = {
            'настройки': Command(DialogAnswer(message='Ваши критерии поиска', keyboard=self.settings_keyboard)),
            'найти': Command(DialogAnswer(message='Ищу...', keyboard=self.start_keyboard)),
            'назад': Command(DialogAnswer(message='Пора искать пару!', keyboard=self.start_keyboard)),
            'возраст': Command(
                DialogAnswer(message='Введите возраст', keyboard=self.settings_keyboard),
                await_answer=True,
                action=self.add_age_to_user
            ),
            'город': Command(
                DialogAnswer(message='Введите город', keyboard=self.settings_keyboard),
                await_answer=True,
                action=self.add_city_to_user
            ),
        }

    # todo Подумать стоит ли инкапсулировать действия в класс
    def add_age_to_user(self, message: str) -> DialogAnswer:
        # Парсинг восраста
        age = re.match(r'\d\d', message)
        if age:
            return DialogAnswer(message=f'Ваш возраст {age.string}', keyboard=self.settings_keyboard)
        else:
            return DialogAnswer(message=f'Не понял ', keyboard=self.settings_keyboard)

    def add_city_to_user(self, message: str) -> DialogAnswer:
        # Парсинг города
        city_names = (city['title'].lower() for city in self.vk_api.database.getCities(country_id=1))
        city = message.lower()
        if city in city_names:
            return DialogAnswer(message=f'Ваш город {city.capitalize()}', keyboard=self.settings_keyboard)
        else:
            return DialogAnswer(message=f'Такого города нет(', keyboard=self.settings_keyboard)

    def input(self, message: str):
        """
        Функция принимающая сообщения пользователя
        :param message: Сообщение
        :return: Ответ пользователю, отправившему сообщение
        """
        # Обработать ответ от пользователя на команду ввода данных
        if self.handler:
            answer = self.handler(message)
            self.handler = None
            return answer

        elif message.lower() in self.commands.keys():
            command = self.commands[message.lower()]

            self.current_answer.keyboard = command.answer.keyboard

            if command.await_answer:
                self.handler = command.action

            return command.answer

        else:
            return self.current_answer
