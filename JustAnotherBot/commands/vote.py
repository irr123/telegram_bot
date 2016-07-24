# coding: utf-8

from .command_interface import AbstractCommand
from .handler import EXIT


class VotingStore(AbstractCommand):
    def invoke(self, *args, **kwargs):
        store = self.workers_container()
        current_user = '{} {}'.format(self.update.message.from_user.first_name,
                                      self.update.message.from_user.last_name)
        if not store.get(self.chat_id):
            store.set(self.chat_id, list())
        if current_user not in store.get(self.chat_id):
            store.get(self.chat_id).append(current_user)


class StopVoteStore(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Stop vote, print result')
        return EXIT


class GetVoters(AbstractCommand):
    def invoke(self, *args, **kwargs):
        store = self.workers_container()
        if store.get(self.chat_id):
            self.answer('List of available users:')
            self.answer(', '.join(store.get(self.chat_id)))
        else:
            self.answer('No users')