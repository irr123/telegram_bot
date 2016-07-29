# coding: utf-8

import re
import numpy as np
from math import floor
from scipy.ndimage import imread
from scipy.misc import toimage


class ImageProcessor(object):
    @staticmethod
    def _maximizer(x, maximum, flag=False):
        val = x/maximum
        ret_val = 254
        if flag and x <= 100:
            ret_val = 0
        else:
            if val < 0.3:
                ret_val = 0
            elif val < 0.5:
                ret_val = 100
        return ret_val

    @staticmethod
    def _normalize_image(image_file):
        image = imread(image_file, flatten=True)
        max_value = np.max(image)
        maximizer_vectorized = np.vectorize(ImageProcessor._maximizer)
        return maximizer_vectorized(maximizer_vectorized(image, max_value),
                                    max_value, True)

    @staticmethod
    def normalize_image(image):
        if isinstance(image, str):
            with open(image, 'rb') as imageFile:
                norm_image = ImageProcessor._normalize_image(imageFile)
        else:
            norm_image = ImageProcessor._normalize_image(image)

        return toimage(norm_image)  # return ndarray


class WorkaroundFixer(object):
    def fix_it(self, data):
        linesByY = dict()
        if len(data) > 0:
            lineList = []
            for region in data:
                for line in region.lines:
                    lineList.append(line)
            for i in range(len(lineList)):
                yCoordinates = set()
                similiarLines = set()
                for j in range(i + 1, len(lineList)):
                    if abs(lineList[i].box.y - lineList[j].box.y) <= 5:
                        yCoordinates.add(lineList[i].box.y)
                        yCoordinates.add(lineList[j].box.y)
                        similiarLines.add(lineList[j])
                        similiarLines.add(lineList[i])
                    if len(yCoordinates) != 0:
                        linesByY.update({floor(sum(yCoordinates)/len(yCoordinates)): list(similiarLines)})

        result = dict()
        lines = linesByY

        regexp = re.compile('\d+\.*[oOоО\s]*')
        for key in lines.keys():
            keytmp = ''
            val = 0
            for i in lines[key]:
                money = regexp.findall(i.text)
                if len(money) > 0:
                    val = str(money[0])
                else:
                    keytmp = keytmp + ' ' + i.text
                result.update({keytmp: int(str(val).split('.')[0])})

        return result
