import random
import re
from enum import Enum

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from app.vk_bot import VkBot
from db.models import VkUser
import db.queries as query


class Command(Enum):

    search = 'Искать'
    settings = 'Настройки'
    age = 'Возраст'
    sex = 'Пол'
    default = 'Главная'
    like = 'Лайк'
    dislike = 'Дизлайк'
    hello = ['привет', 'Привет', 'хай', 'Здорова']


class VKinder:

    @staticmethod
    def get_readable_settings(vk_user: VkUser):
        sex = 'Мужчину' if vk_user.search_sex else 'Женщину'
        return f"Искать: {sex}\n" \
               f"В городе: {vk_user.city_title}\n" \
               f"Возраст: от {vk_user.age_from} до {vk_user.age_to}"

    def __init__(self, bot, vk_requester, db_session):
        self._bot = bot
        self._db_session = db_session
        self._requester = vk_requester

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

        # todo Как избавиться от глобальных переменных функии декоратора?
        #  Либо так либо предовать параметром селф в хендлер
        @self._bot.message_handler(commands=Command.hello.value)
        def hello(message):
            self._bot.keyboard = default_keyboard
            user = query.get_vk_user(self._db_session, message.from_id)
            if user:
                self._bot.reply_to(message, f'Привет {user.firstname} {user.lastname}, пора искать пару!')
            else:
                # todo Возможен случай когда get_user = None. Возможно  профайл  удален?
                user_object = self._requester.get_user(message.from_id)
                if user_object:
                    query.add_vk_user(self._db_session, VkUser(
                        vk_id=user_object['id'],
                        firstname=user_object['first_name'],
                        lastname=user_object['last_name'],
                        sex=True if user_object['sex'] == 2 else False,
                        city_id=user_object['city']['id'],
                        city_title=user_object['city']['title'],
                        search_sex=False if user_object['sex'] == 2 else True,
                        age_from=18,
                        age_to=30
                    ))

                    self._bot.reply_to(message, f'Привет, {user_object["first_name"]} {user_object["last_name"]}!')
                else:
                    self._bot.reply_to(message, f'Привет, кто ты?!')

        @self._bot.message_handler(commands=[Command.age.value])
        def age(message):
            self._bot.register_next_step_handler(message, answer_age_step)
            self._bot.reply_to(message, 'Введите возраст поиска. Например: 18 - 40!')

        def answer_age_step(message):
            # todo Можно сделать регулярку для чтобы парсить разные варианты: от 18 до 40; 18 - 40; 18 40;
            text = message.text.replace(' ', '')
            match = re.match(r'(\d{2})-(\d{2})', text)
            if match:
                age_from = match.group(1)
                age_to = match.group(2)

                query.update_search_age(self._db_session, message.from_id, int(age_from), int(age_to))

                self._bot.keyboard = settings_keyboard
                self._bot.reply_to(message, f'Ваш возраст поиска от {age_from} до {age_to}')
            else:
                self._bot.reply_to(message, 'Не понял')

        @self._bot.message_handler(commands=[Command.sex.value])
        def sex(message):
            self._bot.register_next_step_handler(message, answer_sex_step)
            self._bot.reply_to(message, 'Введите пол поиска. Например: ж')

        def answer_sex_step(message):
            # todo Можно сделать список для чтобы парсить разные варианты: м; ж; мужской; муж; женский; жен; и тд
            text = message.text.replace(' ', '').lower()
            print(text)
            if text == 'ж' or text == 'м':
                sex_id = {'ж': False, 'м': True}

                query.update_search_sex(self._db_session, message.from_id, sex_id[text])

                self._bot.keyboard = settings_keyboard
                self._bot.reply_to(message, f'Ваш пол поиска {text}')
            else:
                self._bot.reply_to(message, 'Не понял')

        @self._bot.message_handler(commands=[Command.default.value])
        def default(message):
            self._bot.keyboard = default_keyboard
            self._bot.reply_to(message, 'Пора заводить новые знакомства!')

        @self._bot.message_handler(commands=[Command.settings.value])
        def settings(message):
            self._bot.keyboard = settings_keyboard

            user = query.get_vk_user(self._db_session, message.from_id)
            text = VKinder.get_readable_settings(user)
            self._bot.reply_to(message, text)

        def like_dislike(message, vk_id):
            self._bot.keyboard = default_keyboard

            if message.text == Command.like.value:
                query.add_user_like(self._db_session, message.from_id, vk_id)
                self._bot.reply_to(message, "Отличный выбор!")
            else:
                query.add_user_dislike(self._db_session, message.from_id, vk_id)
                self._bot.reply_to(message, 'Ты еще найдешь себе друга!')

        @self._bot.message_handler(commands=[Command.search.value])
        def search(message):

            user = query.get_vk_user(self._db_session, message.from_id)
            found_users = self._requester.search_users(
                sex=2 if user.search_sex else 1,
                city=user.city_id,
                age_from=user.age_from,
                age_to=user.age_to
            )

            if found_users['count']:
                self._bot.keyboard = like_keyboard

                # todo Получить из бд dislike id и отфильтровать по ним

                # Получаем id только открытых профайлов и не dislike
                ids = [u['id'] for u in found_users['items'] if not u['is_closed']]
                found_user = self._requester.get_user(random.choice(ids))

                photos = self._requester.get_photos(found_user['id'])
                # Most liked and can add most commented
                photos = sorted(photos, key=lambda p: (p['likes']['count']), reverse=True)[0:3]
                href = f"vk.com/id{found_user['id']}"
                text = f"{found_user['first_name']} {found_user['last_name']}: {href}\n"

                self._bot.register_next_step_handler(message, like_dislike, found_user['id'])
                self._bot.reply_to(message, text)
                for photo in photos:
                    self._bot.send_photo(message.from_id, photo['sizes'][0]['url'])

            else:
                self._bot.keyboard = default_keyboard
                self._bot.reply_to(message, 'Не нашел')

    def start(self):
        self._bot.start_longpoll()
