import random
import re
from enum import Enum
from pprint import pprint

import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import vk_bot

import os
from dotenv import load_dotenv

from vk_user import VkRequester, VkUser


class Command(Enum):

    search = 'Искать'
    settings = 'Настройки'
    age = 'Возраст'
    sex = 'Пол'
    default = 'Главная'


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
    default_keyboard.add_button(Command.search.value, color=VkKeyboardColor.PRIMARY)
    default_keyboard.add_button(Command.settings.value, color=VkKeyboardColor.SECONDARY)

    settings_keyboard = VkKeyboard(one_time=False)
    settings_keyboard.add_button(Command.default.value, color=VkKeyboardColor.SECONDARY)
    settings_keyboard.add_button(Command.age.value, color=VkKeyboardColor.PRIMARY)
    settings_keyboard.add_button(Command.sex.value, color=VkKeyboardColor.PRIMARY)


    @bot.message_handler()
    def start(message):
        if message.from_id not in users:
            print(message.from_id)
            # todo Возможен случай когда get_user = None. Возможно закрыт профайл или удален?
            user = requester.get_user(message.from_id)
            users[message.from_id] = user
            bot.keyboard = default_keyboard
            bot.reply_to(message, f'Привет, {user}!')
        # else:
        #     bot.reply_to(event, 'Пора искать пару')

    @bot.message_handler(commands=[Command.age.value])
    def age(message):
        bot.register_next_step_handler(message, answer_age_step)
        bot.reply_to(message, 'Введите возраст поиска. Например: 18 - 40!')

    def answer_age_step(message):
        # todo Можно сделать регулярку для чтобы парсить разные варианты: от 18 до 40; 18 - 40; 18 40;
        text = message.text.replace(' ', '')
        match = re.match(r'(\d{2})-(\d{2})', text)
        if match:
            age_from = match.group(1)
            age_to = match.group(2)

            user: VkUser = users[message.from_id]
            user.search_settings['age_from'] = age_from
            user.search_settings['end_age'] = age_to

            bot.reply_to(message, f'Ваш возраст поиска от {age_from} до {age_to}')
        else:
            bot.reply_to(message, 'Не понял')

    @bot.message_handler(commands=[Command.sex.value])
    def sex(message):
        bot.register_next_step_handler(message, answer_sex_step)
        bot.reply_to(message, 'Введите пол поиска. Например: ж')

    def answer_sex_step(message):
        # todo Можно сделать список для чтобы парсить разные варианты: м; ж; мужской; муж; женский; жен; и тд
        text = message.text.replace(' ', '').lower()
        print(text)
        if text == 'ж' or text == 'м':

            user: VkUser = users[message.from_id]
            user.search_settings['sex'] = text

            bot.reply_to(message, f'Ваш пол поиска {text}')
        else:
            bot.reply_to(message, 'Не понял')

    @bot.message_handler(commands=[Command.default.value])
    def default(message):
        bot.keyboard = default_keyboard
        bot.reply_to(message, 'Пора искать пару!')

    @bot.message_handler(commands=[Command.settings.value])
    def settings(message):
        bot.keyboard = settings_keyboard
        # todo search settings не канает, так как не читабельный
        user: VkUser = users[message.from_id]
        text = f'Ваши критерии поиска:\n' \
               f'{user.search_settings}'
        bot.reply_to(message, text)


    @bot.message_handler(commands=[Command.search.value])
    def search(message):

        user: VkUser = users[message.from_id]
        found_users = requester.search_users(user.search_settings)
        if found_users['count']:
            # Получаем id только открытых профайлов
            ids = [u['id'] for u in found_users['items'] if not u['is_closed']]
            found_user = requester.get_user(random.choice(ids))

            photos = requester.get_photos(found_user.id)
            # Most liked and commented
            photos = sorted(photos, key=lambda p: (p['likes']['count']), reverse=True)[0:3]
            text = f"{found_user}: {found_user.href}\n"
            bot.reply_to(message, text)
            for photo in photos:
                bot.send_photo(message.from_id, photo['sizes'][-1]['url'])
        else:
            bot.reply_to(message, 'Не нашел')


    bot.start_longpoll()


