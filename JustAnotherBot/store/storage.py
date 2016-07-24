# coding: utf-8


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Store(object, metaclass=Singleton):
    def __init__(self):
        self.storage = dict()

    def __iter__(self):
        return self.storage.keys()

    def get(self, key):
        return self.storage.get(key)

    def set(self, key, value):
        self.storage[key] = value


