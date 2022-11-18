"""
Load image in or get image from video stream
"""
import cv2


def read_saved_image(filename, colour=True, path="cards/"):
    return cv2.imread(
        path + filename + ".jpeg",
        cv2.IMREAD_UNCHANGED if colour else cv2.IMREAD_GRAYSCALE,
    )
