from datetime import datetime

from vk_api import vk_api
from vk_api.vk_api import VkApiMethod




class VkUser:

    def __init__(self, user_id):
        self.user_id = user_id

        # todo Решить проблему с hardcode fields


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
        else:
            return None

    @property
    def sex(self) -> str or None:
        return self.user_object.get('sex')

    @property
    def city(self) -> str or None:
        city = self.user_object.get('city')
        if city:
            return city['title']
        else:
            return None


class VkRequester:
    def __init__(self, token, version='5.130'):
        self.session = vk_api.VkApi(token=token, api_version=version)
        self.api = self.session.get_api()

    def get_user(self, user_id: int, fields):

        user = self.api.users.get(
            user_ids=user_id,
            fields=fields
        )[0]

        return user

    def search_users(self):
        users = self.api.users.search(
            q='Vasya'
        )
        print(users)

