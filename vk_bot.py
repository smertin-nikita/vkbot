
import vk_api.vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

class Handler:
    """
    Class for (next step|reply) handlers
    """

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __getitem__(self, item):
        return getattr(self, item)


class BotMessage:
    def __init__(self, event):
        print(event)
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

        self.next_step_handlers = {}

        self._keyboard = VkKeyboard.get_empty_keyboard()

    @property
    def keyboard(self):
        return self._keyboard

    @keyboard.setter
    def keyboard(self, value: VkKeyboard):
        self._keyboard = value.get_keyboard()

    def register_next_step_handler(self, message, callback, *args, **kwargs):
        """
        Registers a callback function to be notified when new message arrives after `message`.

        Warning: In case `callback` as lambda function, saving next step handlers will not work.

        :param message:     The message for which we want to handle new message in the same chat.
        :param callback:    The callback function which next new message arrives.
        :param args:        Args to pass in callback func
        :param kwargs:      Args to pass in callback func
        """
        from_id = message.from_id
        handler = Handler(callback, *args, **kwargs)
        if from_id in self.next_step_handlers:
            self.next_step_handlers[from_id].append(handler)
        else:
            self.next_step_handlers[from_id] = [handler]

    # def clear_step_handler(self, message):
    #     """
    #     Clears all callback functions registered by register_next_step_handler().
    #
    #     :param message:     The message for which we want to handle new message after that in same chat.
    #     """
    #     chat_id = message.chat.id
    #     self.clear_step_handler_by_chat_id(chat_id)

    def _notify_next_handlers(self, message):
        """
        Description: TBD
        :param message:
        :return:
        """
        handlers = self.next_step_handlers.pop(message.from_id, None)
        if handlers:
            for handler in handlers:
                self._exec_task(handler["callback"], message, *handler["args"], **handler["kwargs"])

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

    def _test_message_handler(self, message_handler, message):
        """
        Test message handler
        :param message_handler:
        :param event:
        :return:
        """
        for message_filter, filter_value in message_handler['filters'].items():
            if filter_value is None:
                continue
            if message.text not in filter_value:
                return False
            print(filter_value, message.text)

        return True

    def message_handler(self, commands=None, **kwargs):

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

    def _notify_command_handlers(self, message):
        """
        Notifies command handlers
        :param handlers:
        :param new_messages:
        :return:
        """
        if len(self.message_handlers) == 0:
            return
        for message_handler in self.message_handlers:
            if self._test_message_handler(message_handler, message):
                self._exec_task(message_handler['function'], message)
                # break

    def start_longpoll(self):
        for event in self.long_poll.listen():
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.message["text"]:
                message = BotMessage(event)
                self._notify_next_handlers(message)
                self._notify_command_handlers(message)

    def send_message(self, peer_id, message, keyboard=None):
        if keyboard:
            keyboard = keyboard.get_keyboard()
        self.vk_api.messages.send(
            peer_id=peer_id,
            message=message,
            random_id=get_random_id(),
            keyboard=self.keyboard
        )

    def reply_to(self, message, text, keyboard=None):
        self.send_message(message.peer_id, text, keyboard)
