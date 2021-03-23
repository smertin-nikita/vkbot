from urllib.parse import urlencode

import vk_api.vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from user_dialog import Dialog
from vk_user import VkUser


class BotMessageEvent:
    def __init__(self, event):
        self.date = event.obj.message['date']
        self.from_id = event.obj.message['from_id']
        self.peer_id = event.obj.message['peer_id']
        self.text = event.obj.message['text']



class Bot:
    def __init__(self, token, group_id):

        self.vk = vk_api.VkApi(token=token, api_version='5.130')
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.users = {}

    def start(self):
        for event in self.long_poll.listen():
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.message["text"]:
                event = BotMessageEvent(event)

                if event.from_id not in self.users:
                    # self.users[event.from_id] = Dialog(self.vk_api, event.from_id)

                # self.send_message(event.peer_id, self.users[event.from_id].input(event.text))

    def send_message(self, peer_id, answer):
        self.vk_api.messages.send(
            peer_id=peer_id,
            message=answer,
            random_id=get_random_id(),
            # keyboard=answer.keyboard.get_keyboard()
        )
