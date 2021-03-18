from random import randrange

import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType


class BotMessageEvent:
    def __init__(self, event):
        self.date = event.object['message']['date']
        self.from_id = event.object['message']['from_id']
        self.peer_id = event.object['message']['peer_id']
        self.text = event.object['message']['text']


class Bot:
    def __init__(self, token, group_id):

        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

    def start(self):
        for event in self.long_poll.listen():
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                event = BotMessageEvent(event)
                print(event)
                # vk_user = self.vk_api.users.get(self.get_peer_id(event))
                self.send_message(event.peer_id, f"{event.peer_id}, я получил ваше сообщение!")


    # def event_handler(self, event_type: VkBotEventType):
    #     self.event_listen.append(event_type)
    #     def decorator(func):
    #         def inner(*args, **kwargs):

    def send_message(self, peer_id, message):
        self.vk_api.messages.send(
            peer_id=peer_id,
            message=message,
            random_id=randrange(10 ** 7)
        )
