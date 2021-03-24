from datetime import datetime
from time import sleep

from vk_api import vk_api
from vk_api.vk_api import VkApiMethod


class VkUser:

    def __init__(self, user_object):
        self.user_object = user_object

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def first_name(self) -> str or None:
        return self.user_object.get('first_name')

    @property
    def last_name(self) -> str or None:
        return self.user_object.get('last_name')

    @property
    def bdate(self) -> str or None:
        return self.user_object.get('bdate')

    @property
    def bdate_to_datetime(self) -> datetime or None:
        if self.bdate:
            return datetime.strptime(self.bdate, "%d.%m.%Y")

    @property
    def sex(self) -> str or None:
        return self.user_object.get('sex')

    @property
    def city(self) -> str or None:
        return self.user_object.get('city')



class VkRequester:
    def __init__(self, token=None, version='5.130'):

        self.session = vk_api.VkApi(token=token, api_version=version)
        self.api = self.session.get_api()
        self.fields = ['first_name', 'last_name', 'bdate', 'sex', 'city']

    def get_user(self, user_id, fields=None):
        sleep(0.24)
        user_object = self.api.users.get(
            user_ids=user_id,
            fields=self.fields
        )[0]
        if user_object:
            return VkUser(user_object)

    def search_users(self, kwargs):
        users = self.api.users.search(
            **kwargs,
            fields=self.fields
        )
        print(users)

