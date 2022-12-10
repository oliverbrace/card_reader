import logging

import cv2
import numpy as np

from card_settings import card_height_width
from image_functions.draw_rectangles import (
    darken_outside_rectangle,
    draw_multiple_rectangles,
    draw_rectangle,
    get_draw_contours,
)
from image_functions.edge_detection import apply_mask, canny_edge_detection
from image_functions.find_rectangles import find_biggest_rectangle, get_rectangles
from image_functions.image_check import get_image_size, rectangle_shape_check
from image_functions.serialize_image import ImageSerialize
from image_functions.transform_image import (
    crop_image,
    gray_add_colour_dimension,
    paste_image,
)


class CardFinder(ImageSerialize):
    """Finds the Card in an Image"""

    def __init__(self):
        self.center_image = None
        self.dimmed_image = None
        self.canny_edge_image = None
        self.found_card_image = None
        self.card_image = None
        self.image_height = None
        self.image_width = None

    def create_canny_edge_image(self):
        if self.center_image is None:
            raise Exception("No canny_edge image")

        self.canny_edge_image = canny_edge_detection(self.center_image, blur=7)
        # height, width = get_image_size(self.canny_edge_image)
        # self.canny_edge_image.shape = (height, width, 1)
        self.canny_edge_image = gray_add_colour_dimension(self.canny_edge_image)

    def find_card(self):
        if self.canny_edge_image is None:
            raise Exception("No canny_edge image")

        rectangles = get_rectangles(
            self.canny_edge_image,
            rect_min_height=self.image_height * 0.4,
            # rect_min_width=self.image_width * 0.4,
            rect_max_height=self.image_height * 0.9,
            rect_max_width=self.image_width * 0.9,
        )
        if len(rectangles) == 0:
            logging.warning("no rectangle")
            return None

        # Check size of card is roughly correct
        for rectangle in rectangles:
            if not rectangle_shape_check(rectangle, card_height_width):
                rectangles.remove(rectangle)

        if len(rectangles) == 0:
            return None

        return find_biggest_rectangle(rectangles)

    def find_center_rectangle(self):
        height = self.image_height
        estimated_width = height / card_height_width
        width_start_point = int(self.image_width / 2 - estimated_width / 2)
        return [width_start_point, 0, int(estimated_width), height]

    def __call__(self):
        center_rectangle = self.find_center_rectangle()
        self.center_image = crop_image(self.original_image, center_rectangle)
        self.dimmed_image = darken_outside_rectangle(
            self.original_image, center_rectangle
        )

        self.create_canny_edge_image()
        rectangle = self.find_card()

        if rectangle is not None:
            self.found_card_image = draw_rectangle(
                self.canny_edge_image, rectangle, thickness=1
            )

            self.card_image = paste_image(
                self.dimmed_image,
                self.found_card_image,
                center_rectangle[0],
                center_rectangle[1],
            )
            # self.output_image(image, f"mixed_card")
        else:
            self.card_image = paste_image(
                self.dimmed_image,
                self.canny_edge_image,
                center_rectangle[0],
                center_rectangle[1],
            )


def run_card_read(card_number):
    card_reader = CardFinder()
    card_reader.load_file_image(f"{card_number}.png")
    card_reader()


def all():
    for card_number in range(1, 9):
        run_card_read(card_number)


run_card_read("video_image")
# all()
