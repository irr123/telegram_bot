# coding: utf-8

import os
from .command_interface import AbstractCommand
from .handler import START, EXIT


class StartConversation(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Ok, now send me photo')
        return START


class GetPic(AbstractCommand):
    @property
    def current_path(self):
        path = os.path.join(self.photo_path, str(self.update.update_id))
        return path

    def invoke(self, *args, **kwargs):
        photo_file = self.bot.getFile(self.update.message.photo[-1].file_id)
        photo_file.download(self.current_path)
        self.answer('Photo received!')
        return EXIT


class PassPic(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Declined')
        return EXIT

