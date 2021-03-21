import vk_api.vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from user_dialog import Dialog
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
        self.create_keyboard()

    def create_keyboard(self):
        self.keyboard = VkKeyboard(one_time=False, inline=False)
        self.keyboard.add_callback_button(
            label="Помощь",
            color=VkKeyboardColor.PRIMARY,
            payload={"type": "help"},
        )

    def start(self):
        for event in self.long_poll.listen():
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:

                print(event.from_id)
                # self.send_message(event.peer_id, self.users[event.from_id].input(event.text))

            elif event.type == VkBotEventType.MESSAGE_EVENT:
                if event.obj.from_id not in self.users:
                    self.users[event.obj.from_id] = event.obj.from_id

                print(event.obj.from_id)
                if event.object.payload.get("type") == "help":
                    self.send_message(event.obj.peer_id, 'help')

    def send_message(self, peer_id, message):
        self.vk_api.messages.send(
            peer_id=peer_id,
            message=message,
            random_id=get_random_id(),
            keyboard=self.keyboard.get_keyboard()
        )
