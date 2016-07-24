# coding: utf-8

from .command_interface import AbstractCommand
from .handler import EXIT, SELECTING, STOP_SELECTING
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class VotingStore(AbstractCommand):
    def invoke(self, *args, **kwargs):
        current_user = '{} {}'.format(self.update.message.from_user.first_name,
                                      self.update.message.from_user.last_name)
        self.workers_container.set_group_user(self.chat_id, current_user)


class GetVoters(AbstractCommand):
    def invoke(self, *args, **kwargs):
        if self.workers_container.get_group_user(self.chat_id):
            self.answer('List of available users:')
            self.answer(', '
                        .join(self.workers_container.get_group_user(self.chat_id))
                        )
        else:
            self.answer('No users')


class SelectVoters(AbstractCommand):
    def invoke(self, *args, **kwargs):
        chat_id = None

        if self.update.message:
            chat_id = self.chat_id

        query = self.update.callback_query
        if query:
            chat_id = query.message.chat_id
            user, pay = query.data.split('\&')
            self.workers_container.add_user_debt(chat_id, user, pay)

        debt = self.workers_container.pop_users_debt(chat_id)
        if not debt:
            self.answer('Products ended, now call "/stop"', chat_id=chat_id)
            return STOP_SELECTING

        if not self.workers_container.get_group_user(chat_id):
            self.answer('Tell me more plz', chat_id=chat_id)
            return SELECTING

        keyboard = list()
        for user in self.workers_container.get_group_user(chat_id):
            keyboard.append(
                [InlineKeyboardButton(user, callback_data=str('{}\&{}'.format(user, debt[1])))]
            )
        self.answer(
            'Still selecting.., who will pay for {}'.format(debt[0]),
            chat_id=chat_id,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SELECTING


class StopSelect(AbstractCommand):
    def invoke(self, *args, **kwargs):
        msg = list()
        res = self.workers_container.get_users_debt(
            self.chat_id
        )
        for user, pay in res.items():
            msg.append('{}: {}'.format(user, pay))
        self.answer('In result: \n{}'.format('\n'.join(msg) if msg else 'Фигня какая-то, считайте вручную'))
        return EXIT


