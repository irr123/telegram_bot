# coding: utf-8


from .command_interface import AbstractCommand

class GetPic(AbstractCommand):
    def invoke(self):
        self.bot.sendMessage(self.update.message.chat_id, text='Need get pic here')






