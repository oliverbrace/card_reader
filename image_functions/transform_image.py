import math

import cv2
import numpy as np

from image_functions.image_check import get_image_size, num_channels_check


def invert_black_white(image):
    return cv2.bitwise_not(image)


def create_grey(image):
    channels = num_channels_check(image)
    if channels < 2:
        raise Exception("Image is already grey")

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


def paste_image(image1, image2, x, y):
    if len(image1.shape) != len(image2.shape):
        raise Exception("Images are not same dimensions")

    height1, width1 = get_image_size(image1)
    height2, width2 = get_image_size(image2)

    if height1 < y + height2 or width1 < x + width2:
        raise Exception("Second image is outside of First image")

    # Copy image 2 onto image 1, starting at x,y
    image1[y : y + height2, x : x + width2] = image2

    # Return the combined result
    return image1


def gray_add_colour_dimension(image):
    height, width = get_image_size(image)

    # Create 8bit color image.
    img_rgb = np.zeros((height, width, 3), dtype=np.uint8)

    # Convert grayscale to color image
    return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB, img_rgb)
