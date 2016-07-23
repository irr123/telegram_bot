#!/usr/bin/env
# coding: utf-8

from telegram.ext import Updater
from JustAnotherBot.config import token
from JustAnotherBot.commands.handler import CustomHandler
from JustAnotherBot.commands.hello_world import Start, Hello
from JustAnotherBot.commands.get_pic import GetPic
from JustAnotherBot.pic_recognizer.main import Recognizer


def init_data():
    return [
        ('start', Start()),
        ('hello', Hello()),
        ('check', GetPic(Recognizer))
    ]


def init_bot(bot_constructor):
    bot = bot_constructor(token)
    data = init_data()
    for d in data:
        bot.dispatcher.add_handler(CustomHandler(*d))

    return bot


if __name__ == '__main__':
    print('Bot started!')
    updater = init_bot(Updater)
    try:
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        print('Stopping bot...')
        exit(0)


