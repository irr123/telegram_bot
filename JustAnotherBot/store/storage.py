# coding: utf-8


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Store(object, metaclass=Singleton):
    def __init__(self):
        self.groups_storage = dict()
        self.parce_checks = dict()
        self.users_debt = dict()

    def __iter__(self):
        return self.groups_storage.keys()

    def get_group_user(self, chat_id):
        return self.groups_storage.get(chat_id)

    def set_group_user(self, chat_id, value):
        if not self.groups_storage.get(chat_id):
            self.groups_storage[chat_id] = list()
        if value not in self.groups_storage[chat_id]:
            self.groups_storage[chat_id].append(value)

    def get_checks(self, chat_id):
        return self.parce_checks.get(chat_id)

    def set_checks(self, chat_id, value):
        self.parce_checks[chat_id] = value

    def add_user_debt(self, chat_id, user_name, value):
        if not self.users_debt.get(chat_id):
            self.users_debt[chat_id] = dict()
        if not self.users_debt[chat_id].get(user_name):
            self.users_debt[chat_id][user_name] = 0
        try:
            self.users_debt[chat_id][user_name] += float(value)
        except ValueError:
            pass

    def get_users_debt(self, chat_id):
        res = self.users_debt[chat_id]
        if res:
            return res
        else:
            return dict()

    def pop_users_debt(self, chat_id):
        try:
            res = self.parce_checks[chat_id].popitem()
        except KeyError:
            res = None
        return res




