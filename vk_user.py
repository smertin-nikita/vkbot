from datetime import date, datetime

from vk_api.vk_api import VkApiMethod


class VkUser:

    def __init__(self, vk_api: VkApiMethod, user_id):
        self.vk_api = vk_api
        self.user_id = user_id

        # todo Решить проблему с hardcode fields
        self.user_object = self.vk_api.users.get(
            user_ids=self.user_id,
            fields=['nickname', 'screen_name', 'first_name', 'last_name' 'sex', 'bdate', 'city', 'country']
        )[0]

    @property
    def first_name(self):
        return self.user_object['first_name']

    @property
    def last_name(self):
        return self.user_object['last_name']

    @property
    def bdate(self):
        return self.user_object['bdate']

    @property
    def city(self):
        return self.user_object['city']

    @property
    def age(self):
        return datetime.now() - self.bdate

