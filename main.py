import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import vk_bot

import os
from dotenv import load_dotenv

from vk_user import VkRequester, VkUser




def get_url_for_token():
    return requests.get(
        url='https://oauth.vk.com/authorize',
        params={
            'client_id': 7697314,
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'display': 'page',
            'scope': ['friends'],
            'response_type': 'token'
        }).url


if __name__ == '__main__':

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
    default_keyboard.add_button('Искать', color=VkKeyboardColor.PRIMARY)
    default_keyboard.add_button('Настройки', color=VkKeyboardColor.SECONDARY)

    settings_keyboard = VkKeyboard(one_time=False)
    settings_keyboard.add_button('Главная', color=VkKeyboardColor.SECONDARY)
    settings_keyboard.add_button('Возраст', color=VkKeyboardColor.PRIMARY)
    settings_keyboard.add_button('Пол', color=VkKeyboardColor.PRIMARY)
    settings_keyboard.add_button('Город', color=VkKeyboardColor.PRIMARY)



    @bot.message_handler()
    def start(event):
        if event.from_id not in users:
            print(event.from_id)
            # todo Возможен случай когда get_user = None.
            user = requester.get_user(event.from_id)
            users[event.from_id] = user
            bot.keyboard = default_keyboard
            bot.reply_to(event, f'Привет, {user}!')
        # else:
            # bot.reply_to(event, 'Пора искать пару')

    @bot.message_handler(commands=['Главная'])
    def default(event):
        bot.keyboard = default_keyboard
        bot.reply_to(event, 'Пора искать пару!')

    @bot.message_handler(commands=['Настройки'])
    def settings(event):
        bot.keyboard = settings_keyboard

        user: VkUser = users[event.from_id]
        message = f'Ваши критерии поиска:' \
                  f'{user.search_settings}'
        bot.reply_to(event, message)


    @bot.message_handler(commands=['Искать'])
    def search(event):

        user: VkUser = users[event.from_id]
        requester.search_users(user.search_settings)
        bot.reply_to(event, 'Нашел')


    bot.start_longpoll()


