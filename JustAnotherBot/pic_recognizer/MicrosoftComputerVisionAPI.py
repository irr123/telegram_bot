from JustAnotherBot.config import MicrosoftCV_API_Key
from JustAnotherBot.config import MicrosoftCV_API_URL
from JustAnotherBot.config import MicrosoftCV_API_MaxNumRetries
import requests
import json

# imageFile = '/home/kiserp/pics/2005-12-06.gif'


class MicrosoftComputerVisionAPI(object):
    _maxNumRetries = MicrosoftCV_API_MaxNumRetries
    _language = 'ru'  # optional
    _detectOrientation = 'True'

    # get raw image binary, return json
    @staticmethod
    def _request_microsoft_cv_api(self, image):
        _requestParameters = {'language': self._language,
                          'detectOrientation': self._detectOrientation}

        _requestHeaders = {'Ocp-Apim-Subscription-Key': MicrosoftCV_API_Key,
                       'Content-Type': 'application/octet-stream'}

    # with open(imageFile, 'rb') as inFile:
    #     rawImage = inFile.read()

        result = ''
        for i in range(self._maxNumRetries):
            try:
                apiRequest = requests.post(MicrosoftCV_API_URL,
                                           params=_requestParameters,
                                           data=image,
                                           headers=_requestHeaders)

                result = apiRequest.json()

                break
            except Exception as ex:
                print(ex)

        return result



