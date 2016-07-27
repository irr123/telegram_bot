from scipy.ndimage import imread
import numpy as np


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

        return norm_image


