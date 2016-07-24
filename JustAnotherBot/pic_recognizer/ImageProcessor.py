from  scipy import misc
import numpy as np

class ImageProcessor:

    @staticmethod
    def _maximizer(x, maximum, flag=False):
        val = x/maximum
        retval = 254
        if flag and x <= 100:
            retval = 0
        else:
            if val < 0.3:
                retval = 0
            elif val < 0.5:
                retval = 100
        return retval

    @staticmethod
    def _maximizer_vectorized(self, func):
        return np.vectorize(func)

    @staticmethod
    def _normalize_image(self, image_file):
        image = misc.imread(image_file, flatten=True)
        max_value = np.max(image)
        return self._maximizer_vectorized(self._maximizer_vectorized(image, max_value), max_value, True)

    @staticmethod
    def normalize_image(self,image):    
        if isinstance(image, str):
            with open(image, 'r') as imageFile:
                return self._normalize_image(imageFile)
        elif isinstance(image, file):
            return self._normalize_image(image)
