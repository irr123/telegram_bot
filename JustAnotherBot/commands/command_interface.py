# coding: utf-8
import os


class AbstractCommand(object):
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'checks_photo')

    def __init__(self, worker=None, *args):
        self.worker = worker
        self.args = args
        self.bot = None
        self.update = None

    def __repr__(self):
        return self.__class__.__name__

    def initialise(self, bot, update):
        self.bot = bot
        self.update = update
        res = self.invoke()
        return res

    def answer(self, msg):
        self.bot.sendMessage(self.update.message.chat_id, text=msg)

    @property
    def chat_id(self):
        return self.update.message.chat_id

    @property
    def photo_path(self):
        dir = os.path.join(self.base_path, str(self.update.message.chat_id))
        if not os.path.isdir(dir):
            os.mkdir(dir)
        return dir

    def invoke(self, *args, **kwargs):
        raise NotImplementedError('Subclass must implement it!', args, kwargs)
