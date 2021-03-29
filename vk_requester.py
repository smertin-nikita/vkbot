from datetime import datetime
from time import sleep

from vk_api import vk_api
from db.models import VkUser


class VkRequester:
    def __init__(self, token=None, version='5.130'):

        self.session = vk_api.VkApi(token=token, api_version=version)
        self.api = self.session.get_api()
        self.fields = ['first_name', 'last_name', 'bdate', 'sex', 'city']

    def search_user(self, user_id, fields=None):
        # sleep(0.24)
        user_object = self.api.users.get(
            user_ids=user_id,
            fields=self.fields
        )[0]
        return user_object

    def get_user(self, user_id, fields=None):
        sleep(0.24)
        user_object = self.api.users.get(
            user_ids=user_id,
            fields=self.fields
        )[0]
        if user_object:
            return VkUser(
                vk_id=user_object['id'],
                firstname=user_object['first_name'],
                lastname=user_object['last_name'],
                sex=True if user_object['sex'] == 2 else False,
                bdate=datetime.strptime(user_object['bdate'], "%d.%m.%Y"),
                city_id=user_object['city']['id'],
                city_title=user_object['city']['title'],
                search_sex=False if user_object['sex'] == 2 else True,
                age_from=18,
                age_to=30
            )

    def search_users(self, **kwargs):
        return self.api.users.search(
            **kwargs,
            has_photo=1,
            sort=1,
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

