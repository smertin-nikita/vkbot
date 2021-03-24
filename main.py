import requests
from flask import request, Flask
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

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

HOST = 'http://127.0.0.1'
PORT = '5000'
DOMAIN = f'{HOST}:{PORT}'

auth_url = requests.get(
    url='https://oauth.vk.com/authorize',
    params={
        'client_id': os.environ.get('CLIENT_ID'),
        'display': 'popup',
        'redirect_uri': f'{DOMAIN}/verify',
        'scope': 'friends',
        'response_type': 'code',
        'v': 5.130
    }
).url



@app.route('/verify')
def get_code():

    code = request.args.get('code')

    response = requests.get(
        url='https://oauth.vk.com/access_token',
        params={
            'client_id': '',
            'client_secret': '',
            'redirect_uri': f'{DOMAIN}/verify',
            'code': code
            })
    response.raise_for_status()

    print(response.json())

    return 'Успешно'


confirmation_code = '03893669'

bot = vk_bot.VkBot(community_token, group_id)

start_keyboard = VkKeyboard(one_time=False)
start_keyboard.add_openlink_button(
    label="Авторизовать",
    link=auth_url,
    payload={"type": "open_link"},
)

users = []

@bot.message_handler()
def start(event):
    if event.from_id not in users:
        bot.reply_to(event, f'Привет! пожалуйста авторизуйся', start_keyboard)
    else:
        bot.reply_to(event, f'Hello, {event.from_id}! пожалуйста авторизуйся')


@app.route('/')
def index():
    return  '!', 200


@app.route('/', methods=['POST'])
def bot():
    # получаем данные из запроса
    data = request.get_json(force=True, silent=True)
    # ВКонтакте в своих запросах всегда отправляет поле type:
    if not data or 'type' not in data:
        return 'not ok'

    # проверяем тип пришедшего события
    if data['type'] == 'confirmation':
        # если это запрос защитного кода
        # отправляем его
        return confirmation_code
    # если же это сообщение, отвечаем пользователю
    elif data['type'] == 'message_new':
        # получаем ID пользователя
        from_id = data['object']['from_id']
        # отправляем сообщение
        bot.send_message(from_id, message='Hello World!')
        # возвращаем серверу VK "ok" и код 200
        return 'ok'

    return 'ok'  # игнорируем другие типы


app.run('0.0.0.0')


