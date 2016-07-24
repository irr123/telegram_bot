from JustAnotherBot.config import MicrosoftCV_API_Key
from JustAnotherBot.config import MicrosoftCV_API_URL
from JustAnotherBot.config import MicrosoftCV_API_MaxNumRetries
from scipy.misc import imsave
import requests
from uuid import UUID
import os

from PIL import Image

# imageFile = '/home/kiserp/pics/2005-12-06.gif'


class MicrosoftComputerVisionAPI(object):
    _maxNumRetries = MicrosoftCV_API_MaxNumRetries
    _language = 'ru'  # optional
    _detectOrientation = 'True'

    class Box(object):

        def __init__(self,x,y,width,height):
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

                # get raw image binary, return json
    @staticmethod
    def _request_microsoft_cv_api(image):
        _requestParameters = {'language': MicrosoftComputerVisionAPI._language,
                          'detectOrientation': True}

        _requestHeaders = {'Ocp-Apim-Subscription-Key': MicrosoftCV_API_Key,
                       'Content-Type': 'application/octet-stream'}

    # with open(imageFile, 'rb') as inFile:
    #     rawImage = inFile.read()
        tmpFileName = 'test.jpg'
        result = dict()

        imsave(tmpFileName, image)

        with open(tmpFileName, 'rb') as tmpFile:
            for i in range(MicrosoftComputerVisionAPI._maxNumRetries):
                try:
                    apiRequest = requests.post(MicrosoftCV_API_URL,
                                               params=_requestParameters,
                                               data=tmpFile,
                                               headers=_requestHeaders)

                    result = apiRequest.json()

                    break
                except Exception as ex:
                    print(ex)
        os.remove(tmpFileName)
        return result

    @staticmethod
    def parse_json_result_to_regions_list(data):
        regions = []
        if 'regions' in data:
            for region_data in data['regions']:
                if 'boundingBox' in region_data:
                    coordinates = region_data['boundingBox'].split(',')
                    box = MicrosoftComputerVisionAPI.Box(coordinates[0], coordinates[1], coordinates[2], coordinates[3])
                    region = MicrosoftComputerVisionAPI.Region([], box)
                    if 'lines' in region_data:
                        for line_data in region_data['lines']:
                            if 'boundingBox' in line_data:
                                coordinates = line_data['boundingBox'].split(',')
                                box = MicrosoftComputerVisionAPI.Box(coordinates[0], coordinates[1], coordinates[2],
                                                                     coordinates[3])
                                line = MicrosoftComputerVisionAPI.Line('', box)
                                separator = ' '
                                if 'words' in line_data:
                                    line.text = separator.join([word['text'] for word in line_data['words']])
                                region.lines.append(line)
                    regions.append(region)

        return regions

    @staticmethod
    def get_data_from_picture(image):
        data = MicrosoftComputerVisionAPI._request_microsoft_cv_api(image)
        return MicrosoftComputerVisionAPI.parse_json_result_to_regions_list(data)


