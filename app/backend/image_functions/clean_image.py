import cv2
import numpy as np


def clean_image(image):
    pass


def opening(image, thresh):
    """erosion followed by dilation - removes noise"""
    kernel = np.ones((thresh, thresh), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def closing(image, thresh=2):
    """dilation followed by erosion - fills in gaps"""
    kernel = np.ones((thresh, thresh), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)


def sharpen(image):
    """Sharpens image"""
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(image, -1, kernel)
