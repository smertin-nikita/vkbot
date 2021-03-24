import requests
from flask import request, Flask

import vk_bot

import os
from dotenv import load_dotenv

from vk_user import VkRequester

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

community_token = os.environ.get("FULL_TOKEN")
group_id = os.environ.get("GROUP_ID")
user_token = os.environ.get('USER_TOKEN')


app = Flask(__name__)


@app.route('/')
def hello_world():
    url = requests.get(
        url='https://oauth.vk.com/authorize',
        params={
            'client_id': '',
            'display': 'popup',
            'redirect_uri': 'http://127.0.0.1:5000/callback',
            'scope': 'friends',
            'response_type': 'code',
            'v': 5.130
        }
    ).url
    href = f"<a href='{url}'>афторизоваться</a>"

    return href


@app.route('/callback')
def get_code():

    code = request.args.get('code')

    response = requests.get(
        url='https://oauth.vk.com/access_token',
        params={
            'client_id': '',
            'client_secret': '',
            'redirect_uri': 'http://127.0.0.1:5000/callback',
            'code': code
            })
    response.raise_for_status()

    print(response.json())

    return 'Успешно'


vk_requester = VkRequester(user_token)

bot = vk_bot.VkBot(community_token, group_id)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f'Hello, {message.from_id}')


bot.start()
