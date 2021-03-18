from random import randrange

import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from vk_user import VkUser


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
        self.users = {}

    def start(self):
        for event in self.long_poll.listen():
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                event = BotMessageEvent(event)

                if event.from_id not in self.users:
                    vk_user = self.add_user(event.from_id)
                    self.send_message(event.peer_id, f"Привет {vk_user['first_name']} {vk_user['last_name']}")
                else:# todo Реализовать юзер диалог. Затем инаплсулировать в класс
                    vk_user = self.users[event.from_id]

                    if not vk_user.get('bdate'):
                        self.send_message(event.peer_id, f"Введите дата рождения (31.12.0000)!")

                    if not vk_user.get('sex'):
                        self.send_message(event.peer_id, f"Введите пол!")

                    if not vk_user.get('city'):
                        self.send_message(event.peer_id, f"Город!")

                # todo Добавить клавиатуру стар поиска когда все данные будут готовы

    def add_user(self, user_id):
        # todo Использовать юзер класс или юзер объект
        new_user = VkUser(user_id)
        self.users[user_id] = new_user
        return new_user

    def get_vk_user_info(self, user_id):
        return self.vk_api.users.get(
            user_ids=user_id,
            fields=['nickname', 'screen_name', 'first_name', 'last_name' 'sex', 'bdate', 'city', 'country']
        )[0]

    def send_message(self, peer_id, message):
        self.vk_api.messages.send(
            peer_id=peer_id,
            message=message,
            random_id=randrange(10 ** 7)
        )
