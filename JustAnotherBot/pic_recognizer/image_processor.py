# coding: utf-8

import re
import numpy as np
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
        self.lineList = list()
        self.linesByY = dict()
        self.yCoordinates = set()
        self.similiarLines = set()

    @staticmethod
    def approximate_y(y):
        ACCURACY = 25
        approximate = float(y) // ACCURACY
        return int(ACCURACY * approximate)

    @staticmethod
    def normalize_num(bad_string):
        bad_letter = {
            'O': '0',
            'o': '0',
            'Б': '6',
            'б': '6',
            'В': '8',
            'в': '8'
        }
        good_letters = list()
        for letter in bad_string:
            if letter in bad_letter:
                good_letters.append(bad_letter.get(letter))
            else:
                good_letters.append(letter)

        return int(''.join(good_letters))

    @staticmethod
    def validate_data(data):
        if not data:
            return False
        if not data.get('regions'):
            return None
        return data['regions']

    def _make_lines(self, data):
        for region in data:
            for line in region.get('lines', list()):
                    self.lineList.extend(
                        line.get('words', list())
                    )

    def _sort_by_y(self):
        for line in self.lineList:
            _y = line.get('boundingBox', '').split(',')[1]
            y = self.approximate_y(_y)
            if y not in self.linesByY:
                self.linesByY[y] = list()
            self.linesByY[y].append(line)

    def _make_new_line(self):
        res = list()
        if not (self.linesByY and isinstance(self.linesByY, dict)):
            print('Error: No lines found!')
        else:
            for y, lines in sorted(self.linesByY.items()):
                tmp = [line.get('text') for line in lines]
                res.append(' '.join(tmp))
        return res

    def _make_result(self, res):
        result = dict()
        first_type = re.compile(r'=(\w+)')
        second_type = re.compile(r'\.{2}(\w+)')
        for num, line in enumerate(res):
            r = first_type.search(line) or second_type.search(line)
            if r:
                try:
                    r = self.normalize_num(r.group(1))
                except ValueError:
                    r = None

                if r:
                    result[res[num-2]] = r

        return result

    def fix_it(self, data):
        valid_data = self.validate_data(data)
        if not valid_data:
            return False

        self._make_lines(valid_data)
        self._sort_by_y()
        res = self._make_new_line()
        result = self._make_result(res)
        print(res)
        return result

