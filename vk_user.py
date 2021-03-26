from datetime import datetime
from pprint import pprint
from time import sleep

from vk_api import vk_api
from vk_api.vk_api import VkApiMethod


class VkUser:

    def __init__(self, user_object):
        self.user_object = user_object
        # default settings
        from_list = [
            user_object.get('activities'),
            user_object.get('interests'),
            user_object.get('music'),
            user_object.get('movies'),
            user_object.get('tv'),
            user_object.get('books'),
            user_object.get('games')
        ]
        print(from_list)

        self.search_settings = {
            'sex': 1 if self.sex == 2 else 2,
            'city': self.city.get('id'),
            'age_from': 18,
            'age_to': 30,
            'has_photo': 1,
            'is_closed': False,
            # 'from_list': ['кино']
        }

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def href(self) -> str:
        url = 'vk.com/id'
        return f"{url}{self.user_object.get('id')}"

    @property
    def id(self) -> str or None:
        return self.user_object.get('id')

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
        self.fields = ['first_name', 'last_name', 'bdate', 'sex', 'city', 'activities', 'interests', 'music', 'movies', 'tv', 'books', 'games',]

    def get_user(self, user_id, fields=None):
        sleep(0.24)
        user_object = self.api.users.get(
            user_ids=user_id,
            fields=self.fields
        )[0]
        if user_object:
            return VkUser(user_object)

    def search_users(self, kwargs):
        return self.api.users.search(
            **kwargs,
            count=1000,
            fields=self.fields
        )

    def get_photos(self, user_id, album_id='profile'):
        """Return photos by number of likes"""

        params = {
            'owner_id': user_id,
            'album_id': album_id,
            'extended': 1,
            'count': 100,
            'photo_sizes': 0
        }

        photos = self.api.photos.get(
            **params
        )
        return photos['items']


