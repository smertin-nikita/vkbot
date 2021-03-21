from datetime import datetime

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
            return datetime.strptime(self.bdate, "DD.MM.YYYY")
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

    # todo return int or str
    @property
    def age(self):
        if self.bdate:
            return datetime.now() - self.bdate_to_datetime
        else:
            return None

