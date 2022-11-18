import cv2

from image_check import num_channels_check


def create_grey(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def gray_to_bl(image, thresh=2):
    channels = num_channels_check(image)
    if channels > 2:
        raise Exception("Image is not grey")

    (_, bl_image) = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
    return bl_image


def crop_image(image, xStart, xEnd, yStart, yEnd):
    return image[yStart:yEnd, xStart:xEnd]
