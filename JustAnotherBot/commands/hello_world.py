# coding: utf-8

from .command_interface import AbstractCommand
from .handler import EXIT


class Test(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Hello World!\nI\'m working :)')
        return EXIT


class Error(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Error happens: {}'.format(self.args[0]))
        return EXIT

