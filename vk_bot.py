from random import randrange

import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType


class Bot:
    def __init__(self, token, group_id):

        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.event_listen = []

    def start(self):
        for event in self.long_poll.listen():
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                print(event)
                self.send_message(event.object['message']['peer_id'], f"{event.object.from_id}, я получил ваше сообщение!")


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
