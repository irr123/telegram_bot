# coding: utf-8


from .command_interface import AbstractCommand


class Start(AbstractCommand):
    def invoke(self):
        self.bot.sendMessage(
            self.update.message.chat_id,
            text='Hello World!'
        )


class Hello(AbstractCommand):
    def invoke(self):
        self.bot.sendMessage(
            self.update.message.chat_id,
            text='Hello {0}'.format(self.update.message.from_user.first_name)
        )




