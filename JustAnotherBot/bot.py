#!/usr/bin/env
# coding: utf-8

import logging
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import ConversationHandler
from JustAnotherBot.config import token
from JustAnotherBot.commands.handler import\
    ObjectCallbackHandler, \
    ObjectCommandHandler, ObjectMessageHandler,\
    UPLOAD_PHOTO, SELECTING, STOP_SELECTING
from JustAnotherBot.commands.hello_world import Error
from JustAnotherBot.commands.get_pic import GetPic,\
    PassPic, StartConversation
from JustAnotherBot.commands.vote import VotingStore, \
    SelectVoters, GetVoters, StopSelect
from JustAnotherBot.pic_recognizer.main import BillData
from JustAnotherBot.store.storage import Store
from JustAnotherBot.store.container import Container


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def init_data():
    return ConversationHandler(
        entry_points=[ObjectCommandHandler('start', StartConversation())],
        states={
            UPLOAD_PHOTO: [
                ObjectMessageHandler([Filters.photo], GetPic(
                    Container(Store(), BillData())
                )),
            ],
            SELECTING: [
                ObjectCommandHandler('select', SelectVoters(
                    Store()
                )),
                ObjectCommandHandler('stop', StopSelect(
                    Store()
                )),
                ObjectCallbackHandler(SelectVoters(
                    Store()
                ))
            ],
            STOP_SELECTING: [
                ObjectCommandHandler('stop', StopSelect(
                    Store()
                ))
            ]
        },
        fallbacks=[ObjectCommandHandler('exit', PassPic())]
    ),\
    [
        ObjectMessageHandler([Filters.text], VotingStore(Store())),
        ObjectCommandHandler('get_voters', GetVoters(Store()))
    ]


def init_bot(bot_constructor):
    bot = bot_constructor(token)
    conv, single = init_data()
    bot.dispatcher.add_handler(conv)
    bot.dispatcher.add_error_handler(Error().invoke)
    for s in single:
        bot.dispatcher.add_handler(s)
    return bot


if __name__ == '__main__':
    print('Bot started!')
    updater = init_bot(Updater)
    # try:
    updater.start_polling()
    updater.idle()
    # except KeyboardInterrupt:
    #     print('Stopping bot...')
    exit(0)


