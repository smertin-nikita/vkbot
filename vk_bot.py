from random import randrange

import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType


class Bot:
    def __init__(self, token, group_id):

        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

    def start(self):
        for event in self.long_poll.listen():
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                vk_user = self.get_user_object(event.message.peer_id)[0]
                self.send_message(event.message.peer_id, f"{vk_user['first_name']} {vk_user['last_name']}, иди за чебурешками!")

    def send_message(self, peer_id, message):
        self.vk_api.messages.send(
            peer_id=peer_id,
            message=message,
            random_id=randrange(10 ** 7)
        )

    def get_user_object(self, user_id):
        return self.vk_api.users.get(
                user_ids=user_id,
                fields=['screen_name', 'sex', 'bdate', 'city', 'country']
            )

