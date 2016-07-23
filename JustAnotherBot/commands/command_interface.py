# coding: utf-8


class AbstractCommand(object):
    def __init__(self, worker=None):
        self.worker = worker
        self.bot = None
        self.update = None

    def initialise(self, bot, update):
        self.bot = bot
        self.update = update
        self.invoke()

    def invoke(self):
        raise NotImplementedError('Subclass must implement it!')
