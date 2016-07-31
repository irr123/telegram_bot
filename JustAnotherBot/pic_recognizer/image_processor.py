# coding: utf-8

import re
import numpy as np
from math import floor
from scipy.ndimage import imread
from scipy.misc import toimage


class ImageProcessor(object):
    BLACK = 0
    WHITE = 254
    LIMIT = 0.45

    @classmethod
    def _maximizer(cls, x, maximum):
        val = x / maximum
        ret_val = cls.WHITE
        if val < cls.LIMIT:
            ret_val = cls.BLACK
        return ret_val

    @classmethod
    def _normalize_image(cls, image_file):
        image = imread(image_file, flatten=True)
        max_value = np.max(image)
        maximizer_vectorized = np.vectorize(cls._maximizer)

        return maximizer_vectorized(
            maximizer_vectorized(image, max_value),
            max_value
        )

    @classmethod
    def normalize_image(cls, image):
        if isinstance(image, str):
            with open(image, 'rb') as imageFile:
                norm_image = cls._normalize_image(imageFile)

        else:
            norm_image = cls._normalize_image(image)

        return toimage(norm_image)


class WorkaroundFixer(object):
    def __init__(self):
        self.lineList = []
        self.linesByY = dict()
        self.yCoordinates = set()
        self.similiarLines = set()

    @staticmethod
    def validate_data(data):
        if not data:
            return False
        if 'regions' not in data:
            return None
        if not data['regions']:
            return None
        return data['regions']

    def _make_lines(self, data):
        for region in data:
            for line in region.get('lines'):
                self.lineList.append(line)

    def _debug_recognizer(self):
        if not self.lineList:
            print('Error: No lines found!')
        else:
            for line in self.lineList:
                print(line)

    def fix_it(self, data):
        result = dict()

        valid_data = self.validate_data(data)
        if not valid_data:
            return False

        self._make_lines(valid_data)
        self._debug_recognizer()

        for i in range(len(self.lineList)):
            for j in range(i + 1, len(self.lineList)):

                if abs(self.lineList[i].box.y - self.lineList[j].box.y) <= 5:
                    self.yCoordinates.add(self.lineList[i].box.y)
                    self.similiarLines.add(self.lineList[i])

                    self.yCoordinates.add(self.lineList[j].box.y)
                    self.similiarLines.add(self.lineList[j])

                if len(self.yCoordinates) != 0:
                    self.linesByY.update({floor(sum(self.yCoordinates)/len(self.yCoordinates)): list(self.similiarLines)})

        # lines = linesByY
        #
        # regexp = re.compile('\d+\.*[oOоО\s]*')
        # for key in lines.keys():
        #     keytmp = ''
        #     val = 0
        #     for i in lines[key]:
        #         money = regexp.findall(i.text)
        #         if len(money) > 0:
        #             val = str(money[0])
        #         else:
        #             keytmp = keytmp + ' ' + i.text
        #         result.update({keytmp: int(str(val).split('.')[0])})

        return result


def _parse_json_result_to_regions_list(self, data):

    regions = []

    for region_data in data['regions']:
        if 'boundingBox' not in region_data:
            continue

        if 'lines' not in region_data:
            continue

        coordinates = region_data['boundingBox'].split(',')
        box = self.Box(*coordinates)
        region = self.Region([], box)

        for line_data in region_data['lines']:
            if 'boundingBox' not in line_data:
                continue

            coordinates = line_data['boundingBox'].split(',')
            box = self.Box(*coordinates)
            line = self.Line('', box)
            separator = ' '
            if 'words' in line_data:
                line.text = separator.join([word['text'] for word in line_data['words']])

            region.lines.append(line)
        regions.append(region)
    return regions