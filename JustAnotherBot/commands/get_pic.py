# coding: utf-8

import os
from io import BytesIO
from requests import get
from .command_interface import AbstractCommand
from .handler import UPLOAD_PHOTO, SELECTING, EXIT


class StartConversation(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Ok, now send me chek\'s photo')
        return UPLOAD_PHOTO


class GetPic(AbstractCommand):
    @property
    def current_path(self):
        path = os.path.join(self.photo_path, str(self.update.update_id))
        return path

    def invoke(self, *args, **kwargs):
        file_img = BytesIO()
        photo_file = self.bot.getFile(self.update.message.photo[-1].file_id)
        # photo_file.download(file_img)
        r = get(photo_file.file_path)
        file_img.write(r.content)
        file_img.seek(0)  # move ptr!


        self.workers_container.group_storage.set_checks(
            self.chat_id,
            self.workers_container.img_recognizer.get_data_from_bill_picture(file_img)
            # self.workers_container.img_recognizer.get_data_from_bill_picture(self.current_path)
        )

        self.answer('Photo received!\nNow you can call "/select"')
        return SELECTING


class PassPic(AbstractCommand):
    def invoke(self, *args, **kwargs):
        self.answer('Declined')
        return EXIT

