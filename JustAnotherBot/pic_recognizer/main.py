# coding: utf-8
from pic_recognizer.ImageProcessor import ImageProcessor
from pic_recognizer.MicrosoftComputerVisionAPI import MicrosoftComputerVisionAPI as mscvapi


class billData(object):

    def __init__(self):
        self.items = dict()
        self.billNumber = ''
        self.organizationName = ''
        self.timeStamp = ''
        self.dateFromBill = ''
        self.timeFromBill = ''
        self.operatorID = ''
        self.organizationID = ''
        self.total = 0

    def test_filler(self, image):
        self.items = {'Brown Sugar': 234, 'Coffee': 34, 'sousage': 324, 'doll': 32, 'гренки': 232 ,'漢語': 329}

    def get_data_from_bill_picture(self,image):
        normalizedImage = ImageProcessor.normalize_image(image)







