# coding: utf-8

from .command_interface import AbstractCommand
from .handler import EXIT


class Test(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Hello World!\nI\'m working :)')
        return EXIT


class Error(AbstractCommand):
    def invoke(self, *args, **kwargs):
        try:
            err = args[2].message
        except IndexError:
            err = 'Undefined error'
        self.answer('Error happens: {}'.format(err))
        return EXIT

