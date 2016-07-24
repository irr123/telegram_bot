from scipy.misc import imread
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
                return ImageProcessor._normalize_image(imageFile)
        else:
            return ImageProcessor._normalize_image(image)
