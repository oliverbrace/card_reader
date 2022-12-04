"""
Load image in or get image from video stream
"""
import cv2

from card_settings import (
    text_h_percentage,
    text_s_h_percentage,
    text_s_w_percentage,
    text_w_percentage,
)


def read_saved_image(filename, colour=True, path="cards/"):
    return cv2.imread(
        path + filename,
        cv2.IMREAD_UNCHANGED if colour else cv2.IMREAD_GRAYSCALE,
    )


def find_text_rect(self):
    # Assumes height is roughly correct
    rectangle = []
    height = self.card_image.shape[0]
    rectangle.append(height * text_s_w_percentage)
    rectangle.append(height * text_s_h_percentage)
    rectangle.append(height * text_w_percentage)
    rectangle.append(height * text_h_percentage)
    rectangle = tuple(rectangle)
    return rectangle
