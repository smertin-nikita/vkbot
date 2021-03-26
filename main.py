import re
from enum import Enum

import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import vk_bot

import os
from dotenv import load_dotenv

from vk_user import VkRequester, VkUser


class Command(Enum):

    find = '/Искать'
    settings = '/Настройки'
    age = '/Возраст'
    sex = '/Пол'
    default = '/Главная'


def get_url_for_token():
    print(requests.get(
        url='https://oauth.vk.com/authorize',
        params={
            'client_id': 7697314,
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'display': 'page',
            'scope': ['friends'],
            'response_type': 'token'
        }).url)
    exit(0)


if __name__ == '__main__':
    # get_url_for_token()

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    community_token = os.environ.get("FULL_TOKEN")
    group_id = os.environ.get("GROUP_ID")
    user_token = os.environ.get('USER_TOKEN')

    bot = vk_bot.VkBot(community_token, group_id)
    requester = VkRequester(token=user_token)

    users = {}

    default_keyboard = VkKeyboard(one_time=False)
    default_keyboard.add_button(Command.find.value, color=VkKeyboardColor.PRIMARY)
    default_keyboard.add_button(Command.settings.value, color=VkKeyboardColor.SECONDARY)

    settings_keyboard = VkKeyboard(one_time=False)
    settings_keyboard.add_button(Command.default.value, color=VkKeyboardColor.SECONDARY)
    settings_keyboard.add_button(Command.age.value, color=VkKeyboardColor.PRIMARY)
    settings_keyboard.add_button(Command.sex.value, color=VkKeyboardColor.PRIMARY)


    @bot.message_handler()
    def start(event):
        if event.from_id not in users:
            print(event.from_id)
            # todo Возможен случай когда get_user = None. Возможно закрыт профайл или удален?
            user = requester.get_user(event.from_id)
            users[event.from_id] = user
            bot.keyboard = default_keyboard
            bot.reply_to(event, f'Привет, {user}!')
        # else:
        #     bot.reply_to(event, 'Пора искать пару')

    @bot.message_handler(commands=[Command.age.value])
    def age(event):
        bot.register_next_step_handler(event, process_age_step)
        bot.reply_to(event, 'Введите возраст поиска. Например: 18 - 40!')

    def process_age_step(message):
        # todo Можно сделать регулярку для чтобы парсить разные варианты: от 18 до 40; 18 - 40; 18 40;
        text = message.text.replace(' ', '')
        match = re.match(r'(\d{2})-(\d{2})', text)
        if match:
            start_age = match.group(1)
            end_age = match.group(2)

            bot.reply_to(message, f'Ваш возраст поиска от {start_age} до {end_age}')
        else:
            bot.reply_to(message, 'Не понял')


    @bot.message_handler(commands=[Command.default.value])
    def default(event):
        bot.keyboard = default_keyboard
        bot.reply_to(event, 'Пора искать пару!')

    @bot.message_handler(commands=[Command.settings.value])
    def settings(event):
        bot.keyboard = settings_keyboard
        # todo search settings не канает, так как не читабельный
        user: VkUser = users[event.from_id]
        message = f'Ваши критерии поиска:\n' \
                  f'{user.search_settings}'
        bot.reply_to(event, message)


    @bot.message_handler(commands=[Command.find.value])
    def search(event):

        user: VkUser = users[event.from_id]
        requester.search_users(user.search_settings)
        bot.reply_to(event, 'Нашел')


    bot.start_longpoll()


