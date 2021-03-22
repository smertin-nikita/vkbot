import vk_api.vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from user_dialog import Dialog
from vk_user import VkUser


class BotMessageEvent():
    def __init__(self, event):
        self.date = event.object['message']['date']
        self.from_id = event.object['message']['from_id']
        self.peer_id = event.object['message']['peer_id']
        self.text = event.object['message']['text']



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
                print(event.obj.message['from_id'])

                if event.obj.message['from_id'] not in self.users:
                    self.users[event.obj.message['from_id']] = Dialog(event.obj.message['from_id'])

                self.send_message(event.obj.message['peer_id'], self.users[event.obj.message['from_id']].input(event.obj.message['text']))

            # elif event.type == VkBotEventType.MESSAGE_EVENT:
            #     print('кнопка')
            #     if event.object.payload.get("type") == "settings":
            #         self.edit_message(event.obj.peer_id, 'ТЕСТ', event.obj.conversation_message_id, self.settings_keyboard)

    def edit_message(self, peer_id, message, conversation_message_id, keyboard):
        self.vk_api.messages.edit(
            peer_id=peer_id,
            message=message,
            conversation_message_id=conversation_message_id,
            keyboard=keyboard.get_keyboard()
        )

    def send_message(self, peer_id, answer):
        self.vk_api.messages.send(
            peer_id=peer_id,
            message=answer.message,
            random_id=get_random_id(),
            keyboard=answer.keyboard.get_keyboard()
        )
