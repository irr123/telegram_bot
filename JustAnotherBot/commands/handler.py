# coding: utf-8


from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler

UPLOAD_PHOTO = 0
VOTING = 1
SELECTING = 2
STOP_SELECTING = 3
EXIT = ConversationHandler.END


class ObjectCommandHandler(CommandHandler):
    def __init__(self, command, callback, allow_edited=False,
                 pass_args=False, pass_update_queue=False):

        super().__init__(command, callback.initialise, allow_edited=allow_edited,
                         pass_args=pass_args, pass_update_queue=pass_update_queue)


class ObjectMessageHandler(MessageHandler):
    def __init__(self, filters, callback, allow_edited=False, pass_update_queue=False):

        super().__init__(filters, callback.initialise, allow_edited=allow_edited,
                         pass_update_queue=pass_update_queue)


class ObjectCallbackHandler(CallbackQueryHandler):
    def __init__(self, callback, pass_update_queue=False, pass_job_queue=False):

        super().__init__(callback.initialise, pass_job_queue=pass_job_queue,
                         pass_update_queue=pass_update_queue)



