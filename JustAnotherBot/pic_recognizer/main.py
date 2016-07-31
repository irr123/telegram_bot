# coding: utf-8

from JustAnotherBot.pic_recognizer.ms_vision_api import MicrosoftComputerVisionAPI
from JustAnotherBot.pic_recognizer.image_processor import ImageProcessor, WorkaroundFixer


class BillData(object):
    def __init__(self, normalizer=ImageProcessor,
                 recognizer=MicrosoftComputerVisionAPI,
                 adjuster=WorkaroundFixer):

        self.normalizer = normalizer()
        self.recognizer = recognizer()
        self.adjuster = adjuster()

    def get_data_from_bill_picture(self, image):
        norm_image = self.normalizer.normalize_image(image)
        rec_data = self.recognizer.get_data_from_picture(norm_image)
        result = self.adjuster.fix_it(rec_data)
        return result


class FakeBillData(object):
    def get_data_from_picture(self, image):
        return {'Brown Sugar': 234, 'Coffee': 34, 'sousage': 324, 'doll': 32, 'гренки': 232, '漢語': 329}


if __name__ == '__main__':
    """For tests recognizer
    """
    from os import path

    source = path.join(path.dirname(path.realpath(__file__)), 'fixtures/check2.jpg')
    recognizer = BillData()
    result = recognizer.get_data_from_bill_picture(source)
    print('Input: {}\nOutput: {}'.format(source, result))








