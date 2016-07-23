# coding: utf-8

from .command_interface import AbstractCommand
from .handler import EXIT, VOTING


class VotingStore(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Voting...')
        return VOTING


class StopVoteStore(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Stop vote, print result')
        return EXIT
