# coding: utf-8

from JustAnotherBot.config import MicrosoftCV_API_Key
from JustAnotherBot.config import MicrosoftCV_API_URL
from JustAnotherBot.config import MicrosoftCV_API_MaxNumRetries
import requests
from io import BytesIO


class AbstractRecognizer(object):
    class Box(object):
        def __init__(self, x, y, width, height):
            self.x = int(x)
            self.y = int(y)
            self.width = int(width)
            self.height = int(height)

    class Line(object):
        def __init__(self, text, box):
                self.text = text
                self.box = box

    class Region(object):
        def __init__(self, lines, box):
            self.lines = lines
            self.box = box

    @staticmethod
    def _prepare_img(img):
        file_img = BytesIO()
        img.save(file_img, format='JPEG')
        file_img.seek(0)  # move ptr!
        return file_img

    def get_data_from_picture(self, image):
        raise NotImplemented


class MicrosoftComputerVisionAPI(AbstractRecognizer):
    def __init__(self):
        self._maxNumRetries = MicrosoftCV_API_MaxNumRetries
        self._language = 'ru'  # optional

    def _request_microsoft_cv_api(self, image):
        file_img = self._prepare_img(image)
        # with open('image.jpg', 'wb') as f:
        #     f.write(file_img.read())
        #     file_img.seek(0)
        request_parameters = {
            'language': self._language,
            'detectOrientation': True
        }
        request_headers = {
            'Ocp-Apim-Subscription-Key': MicrosoftCV_API_Key,
            'Content-Type': 'application/octet-stream'
        }
        result = None
        for i in range(self._maxNumRetries):
            try:
                apiRequest = requests.post(MicrosoftCV_API_URL,
                                           params=request_parameters,
                                           data=file_img.read(),
                                           headers=request_headers)
                result = apiRequest.json()
                break
            except Exception as ex:
                print(ex)

        return result

    def get_data_from_picture(self, image):
        return self._request_microsoft_cv_api(image)



