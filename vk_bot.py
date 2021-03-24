
import vk_api.vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType



class BotMessageEvent:
    def __init__(self, event):
        self.date = event.obj.message['date']
        self.from_id = event.obj.message['from_id']
        self.peer_id = event.obj.message['peer_id']
        self.text = event.obj.message['text']


class VkBot:
    def __init__(self, token, group_id):

        self.vk = vk_api.VkApi(token=token, api_version='5.130')
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

        self.message_handlers = []

        self.users = {}
        self.start_keyboard = VkKeyboard(one_time=False)
        self.start_keyboard.add_button('Найти', color=VkKeyboardColor.POSITIVE)
        self.start_keyboard.add_openlink_button(
            label="Откртыть Url",
            link="https://vk.com/dev/bots_docs_5",
            payload={"type": "open_link", "link": "https://vk.com/dev/bots_docs_5"},
        )

    @staticmethod
    def _build_handler_dict(handler, **filters):
        """
        Builds a dictionary for a handler
        :param handler:
        :param filters:
        :return:
        """
        return {
            'function': handler,
            'filters': filters
        }

    def _exec_task(self, task, *args, **kwargs):
        task(*args, **kwargs)

    def _test_message_handler(self, message_handler, event):
        """
        Test message handler
        :param message_handler:
        :param event:
        :return:
        """
        for message_filter, filter_value in message_handler['filters'].items():
            if filter_value is None:
                continue
            if not event.text in filter_value:
                return False
            print(filter_value, event.text)

        return True

    def message_handler(self, commands=None, regexp=None, func=None, content_types=None, **kwargs):

        if content_types is None:
            content_types = ["text"]

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler,
                                                    commands=commands,
                                                    **kwargs)
            self.add_message_handler(handler_dict)
            return handler

        return decorator

    def add_message_handler(self, handler_dict):
        """
        Adds a message handler
        :param handler_dict:
        :return:
        """
        self.message_handlers.append(handler_dict)

    def start(self):
        for event in self.long_poll.listen():
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.message["text"]:
                event = BotMessageEvent(event)
                print(event.text)
                for message_handler in self.message_handlers:
                    if self._test_message_handler(message_handler, event):
                        print('work')
                        self._exec_task(message_handler['function'], event)


    def send_message(self, peer_id, answer):
        self.vk_api.messages.send(
            peer_id=peer_id,
            message=answer,
            random_id=get_random_id(),
            keyboard=self.start_keyboard.get_keyboard()
        )

    def reply_to(self, event, answer):
        self.vk_api.messages.send(
            peer_id=event.peer_id,
            message=answer,
            random_id=get_random_id(),
            keyboard=self.start_keyboard.get_keyboard()
        )
