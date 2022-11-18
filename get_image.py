"""
Load image in or get image from video stream
"""
import cv2


def read_saved_image(filename, path="cards/"):
    return cv2.imread(path + filename + ".jpeg", cv2.IMREAD_GRAYSCALE)
