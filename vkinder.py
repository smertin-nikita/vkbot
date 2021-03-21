from abc import ABC


class KinderBot(ABC):
    """

    """
    def __init__(self):
        # Оправшиваемые поля у пользователя
        self.fields = ['first_name', 'last_name', 'sex', 'city', 'bdate']
        # todo Реализовать базу данных
        self.users = []

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        self._fields = value
