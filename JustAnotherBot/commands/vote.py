# coding: utf-8

from .command_interface import AbstractCommand
from .handler import EXIT


class VotingStore(AbstractCommand):
    def invoke(self, *args, **kwargs):
        current_user = '{} {}'.format(self.update.message.from_user.first_name,
                                      self.update.message.from_user.last_name)
        if not self.workers_container.get(self.chat_id):
            self.workers_container.set(self.chat_id, list())
        if current_user not in self.workers_container.get(self.chat_id):
            self.workers_container.get(self.chat_id).append(current_user)


class GetVoters(AbstractCommand):
    def invoke(self, *args, **kwargs):
        if self.workers_container.get(self.chat_id):
            self.answer('List of available users:')
            self.answer(', '
                        .join(self.workers_container.get(self.chat_id))
                        )
        else:
            self.answer('No users')


class SelectVoters(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Stop vote, print result')
        return EXIT





