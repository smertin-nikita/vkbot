import random
import re
from enum import Enum
from pprint import pprint

import psycopg2
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import vk_bot

import os
from dotenv import load_dotenv

from db.models import VkUser, Base, UserLike, UserDislike
from vk_requester import VkRequester, VkUser


class Command(Enum):

    search = 'Искать'
    settings = 'Настройки'
    age = 'Возраст'
    sex = 'Пол'
    default = 'Главная'
    like = 'Лайк'
    dislike = 'Дизлайк'
    hello = ['привет', 'Привет', 'хай', 'Здорова']


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





def get_readable_settings(vk_user: VkUser):
    sex = 'Мужчину' if vk_user.search_sex else 'Женщину'
    return f"Искать: {sex}\n" \
           f"В городе: {vk_user.city_title}\n" \
           f"Возраст: от {vk_user.age_from} до {vk_user.age_to}"


if __name__ == '__main__':
    # get_url_for_token()

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    community_token = os.environ.get("FULL_TOKEN")
    group_id = os.environ.get("GROUP_ID")
    user_token = os.environ.get('USER_TOKEN')
    db_user = os.environ.get('DATABASE_USER')
    db_password = os.environ.get('DATABASE_PASSWORD')
    db_host = os.environ.get('DATABASE_HOST')
    db_port = os.environ.get('DATABASE_PORT')
    db_name = os.environ.get('DATABASE_NAME')

    bot = vk_bot.VkBot(community_token, group_id)
    requester = VkRequester(token=user_token)

    engine = create_engine(
        f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )
    # Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db_session = session_factory()
    users = {}

    default_keyboard = VkKeyboard(one_time=False)
    default_keyboard.add_button(Command.search.value, color=VkKeyboardColor.PRIMARY)
    default_keyboard.add_button(Command.settings.value, color=VkKeyboardColor.SECONDARY)

    settings_keyboard = VkKeyboard(one_time=False)
    settings_keyboard.add_button(Command.default.value, color=VkKeyboardColor.SECONDARY)
    settings_keyboard.add_button(Command.age.value, color=VkKeyboardColor.PRIMARY)
    settings_keyboard.add_button(Command.sex.value, color=VkKeyboardColor.PRIMARY)

    like_keyboard = VkKeyboard(one_time=False)
    like_keyboard.add_button(Command.like.value, color=VkKeyboardColor.POSITIVE)
    like_keyboard.add_button(Command.dislike.value, color=VkKeyboardColor.NEGATIVE)


    @bot.message_handler(commands=Command.hello.value)
    def hello(message):
        user = get_vk_user(db_session, message.from_id)
        # todo Как избавиться от глобальных переменных функии декоратора??
        if user:
            bot.keyboard = default_keyboard
            bot.reply_to(message, f'Привет {user.firstname} {user.lastname}, пора искать пару!')
        else:
            print(message.from_id)
            # todo Возможен случай когда get_user = None. Возможно  профайл  удален?
            user = requester.get_user(message.from_id)
            add_vk_user(db_session, user)

            bot.keyboard = default_keyboard
            bot.reply_to(message, f'Привет, {user.firstname} {user.lastname}!')

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

            update_search_age(db_session, message.from_id, int(age_from), int(age_to))

            bot.keyboard = settings_keyboard
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
            sex_id = {'ж': False, 'м': True}

            update_search_sex(db_session, message.from_id, sex_id[text])

            bot.keyboard = settings_keyboard
            bot.reply_to(message, f'Ваш пол поиска {text}')
        else:
            bot.reply_to(message, 'Не понял')

    @bot.message_handler(commands=[Command.default.value])
    def default(message):
        bot.keyboard = default_keyboard
        bot.reply_to(message, 'Пора заводить новые знакомства!')

    @bot.message_handler(commands=[Command.settings.value])
    def settings(message):
        bot.keyboard = settings_keyboard

        user = get_vk_user(db_session, message.from_id)
        text = get_readable_settings(user)
        bot.reply_to(message, text)

    def like_dislike(message, vk_id):
        bot.keyboard = default_keyboard

        if message.text == Command.like:
            add_user_like(db_session, message.from_id, vk_id)
            bot.reply_to(message, "Отличный выбор!")
        else:
            add_user_dislike(db_session, message.from_id, vk_id)
            bot.reply_to(message, 'Ты еще найдешь себе друга!')


    @bot.message_handler(commands=[Command.search.value])
    def search(message):

        user = get_vk_user(db_session, message.from_id)
        found_users = requester.search_users(
            sex=2 if user.search_sex else 1,
            city=user.city_id,
            age_from=user.age_from,
            age_to=user.age_to
        )

        if found_users['count']:
            bot.keyboard = like_keyboard

            # todo Получить из бд dislike id и отфильтровать по ним

            # Получаем id только открытых профайлов и не dislike
            ids = [u['id'] for u in found_users['items'] if not u['is_closed']]
            found_user = requester.search_user(random.choice(ids))

            photos = requester.get_photos(found_user['id'])
            # Most liked and commented
            photos = sorted(photos, key=lambda p: (p['likes']['count']), reverse=True)[0:3]
            href = f"vk.com/id{found_user['id']}"
            text = f"{found_user['first_name']} {found_user['last_name']}: {href}\n"

            bot.register_next_step_handler(message, like_dislike, found_user['id'])
            bot.reply_to(message, text)
            for photo in photos:
                bot.send_photo(message.from_id, photo['sizes'][0]['url'])

        else:
            bot.keyboard = default_keyboard
            bot.reply_to(message, 'Не нашел')


    bot.start_longpoll()


