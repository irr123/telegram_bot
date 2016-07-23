# coding: utf-8


from telegram.ext import CommandHandler


class CustomHandler(CommandHandler):
    def __init__(self, command, callback, allow_edited=False,
                 pass_args=False, pass_update_queue=False):

        super().__init__(command, callback.initialise, allow_edited=allow_edited,
                         pass_args=pass_args, pass_update_queue=pass_update_queue)



