# coding: utf-8
from pic_recognizer.ImageProcessor import ImageProcessor
from pic_recognizer.MicrosoftComputerVisionAPI import MicrosoftComputerVisionAPI as mscvapi
from math import floor

class BillData(object):
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
        return {'Brown Sugar': 234, 'Coffee': 34, 'sousage': 324, 'doll': 32, 'гренки': 232,'漢語': 329}

    @staticmethod
    def get_data_from_bill_picture(image):
        normalizedImage = ImageProcessor.normalize_image(image)
        regions = mscvapi.get_data_from_picture(normalizedImage)
        linesByY = dict()
        if len(regions) > 0:
            lineList = []
            for region in regions:
                lineList.append(region.lines)
            for i in range(len(lineList)):
                yCoordinates = set()
                similiarLines = set()
                for j in range(i + 1, len(lineList)):
                    if abs(lineList[i].box.y - lineList[j].box.y) >= 5:
                        yCoordinates.add(lineList[i].box.y)
                        yCoordinates.add(lineList[j].box.y)
                        similiarLines.add(lineList[j])
                        similiarLines.add(lineList[i])
                    linesByY.update({floor(sum(yCoordinates)/len(yCoordinates)): list(similiarLines)})
        return linesByY





lines = BillData.get_data_from_bill_picture('/tmp/634802986_2730330.jpg')
for line in lines:
    for key in lines.keys():
        for a in lines[key]:
            print('y = %d: %s - %d,%d,%d,%d'%(key, a.text, a.box.x, a.box.y, a.box.width, a.box.height))
            print('\n')







