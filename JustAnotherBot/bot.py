#!/usr/bin/env
# coding: utf-8

from telegram.ext import Updater, CommandHandler, MessageHandler
from JustAnotherBot.config import token
from JustAnotherBot.commands.hello_world import start, hello
from JustAnotherBot.commands.get_pic import get_pic

initial_data = [
    ('start', start),
    ('hello', hello),
    ('check', get_pic)
]


def init_bot(bot_constructor):
    bot = bot_constructor(token)
    for data in initial_data:
        bot.dispatcher.add_handler(CommandHandler(*data))

    return bot


if __name__ == '__main__':
    print('Bot started')
    updater = init_bot(Updater)
    try:
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        print('Stopping bot')
        exit(0)


