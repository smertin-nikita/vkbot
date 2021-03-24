import requests
from flask import request, Flask
from vk_api import vk_api
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

    search_keyboard = keyboard = VkKeyboard(one_time=False)
    search_keyboard.add_button('Искать', color=VkKeyboardColor.SECONDARY)

    @bot.message_handler()
    def start(event):
        if event.from_id not in users:
            print(event.from_id)
            # todo Возможен случай когда get_user = None.
            user = requester.get_user(event.from_id)
            users[event.from_id] = user
            bot.reply_to(event, f'Привет, {user}!')
        else:
            bot.reply_to(event, 'Пора искать пару', search_keyboard)

    @bot.message_handler(commands=['Искать'])
    def search(event):
        user: VkUser = users[event.from_id]
        params = {
            'sex': 1 if user.sex == 2 else 2,
            'city': user.city.get('id'),
        }
        requester.search_users(params)
        bot.reply_to(event, 'Нашел', search_keyboard)

    bot.start_longpoll()


