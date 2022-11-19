import math

import cv2

from image_check import num_channels_check


def invert_black_white(image):
    return cv2.bitwise_not(image)


def create_grey(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def grey_to_bl(image, thresh=2):
    channels = num_channels_check(image)
    if channels > 2:
        raise Exception("Image is not grey")

    (_, bl_image) = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
    return bl_image


def old_crop_image(image, xStart, xEnd, yStart, yEnd):
    return image[yStart:yEnd, xStart:xEnd]


def crop_image(image, rect):
    """_summary_

    Args:
        image (_type_): _description_
        rect (List): (xStart, yStart, width, height)

    Returns:
        _type_: _description_
    """
    scale_img_size = 0
    xStart = int(rect[0] * (1 - scale_img_size))
    xEnd = math.ceil((rect[0] + rect[2]) * (1 + scale_img_size))
    yStart = int(rect[1] * (1 - scale_img_size))
    yEnd = math.ceil((rect[1] + rect[3]) * (1 + scale_img_size))
    return image[yStart:yEnd, xStart:xEnd]
