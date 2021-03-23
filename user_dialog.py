import re
from enum import Enum

import requests
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

    def __init__(self, vk_api, vk_user: VkUser):
        self.user = vk_user
        self.handler = None
        self.api = vk_api

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
            'настройки': Command(
                DialogAnswer(
                    message=f'Ваши критерии поиска:\n'
                            f'Возраст: {self.user.bdate}\n'
                            f'Пол: {self.user.sex}\n'
                            f'Город: {self.user.city}\n',
                    keyboard=self.settings_keyboard)
            ),
            'найти': Command(
                DialogAnswer(message='Ищу...', keyboard=self.start_keyboard),
                action=self.find_users
            ),
            'назад': Command(DialogAnswer(message='Пора искать пару!', keyboard=self.start_keyboard)),
            'возраст': Command(
                DialogAnswer(message='Укажите дату рождения: https://vk.com/edit', keyboard=self.settings_keyboard)
            ),
            'город': Command(
                DialogAnswer(message='Укажите город проживания: https://vk.com/edit?act=contacts', keyboard=self.settings_keyboard),
            ),
            'пол': Command(
                DialogAnswer(message='Укажите ваш пол: https://vk.com/edit', keyboard=self.settings_keyboard),
            ),
        }


    def find_users(self):
        data = self.api.users.search(
            params={
                'q':'Vasya Babich'
            })
        print(data)

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
            elif command.action:
                command.action()

            return command.answer

        else:
            return self.current_answer
