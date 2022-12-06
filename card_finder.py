import logging

import cv2

from card_settings import card_height_width
from image_functions.draw_rectangles import draw_rectangle
from image_functions.edge_detection import apply_mask, simple_edge_mask
from image_functions.find_rectangles import find_biggest_rectangle, get_rectangles
from image_functions.image_check import rectangle_shape_check
from image_functions.transform_image import crop_image
from serialize_image import ImageSerialize


class CardFinder(ImageSerialize):
    """Finds the Card in an Image"""

    def __init__(self):
        self.border_image = None
        self.found_card_image = None
        self.card_image = None
        self.image_height = None
        self.image_width = None

    def find_card(self):
        mask = simple_edge_mask(self.original_image)
        self.border_image = apply_mask(self.original_image, mask)
        rectangles = get_rectangles(
            self.border_image,
            rect_min_height=self.image_height * 0.4,
            rect_min_width=self.image_width * 0.4,
            rect_max_height=self.image_height * 0.9,
            rect_max_width=self.image_width * 0.9,
        )
        if len(rectangles) == 0:
            logging.warning("No rectangles found")
            return None

        # Check size of card is roughly correct
        for rectangle in rectangles:
            if not rectangle_shape_check(rectangle, card_height_width):
                rectangles.remove(rectangle)

        if len(rectangles) == 0:
            logging.warning("No rectangles found")
            return None

        return find_biggest_rectangle(rectangles)

    def __call__(self):
        rectangle = self.find_card()

        if rectangle is not None:
            self.found_card_image = draw_rectangle(self.original_image, rectangle)
            self.card_image = crop_image(self.original_image, rectangle)


def run_card_read(card_number):
    card_reader = CardFinder()
    card_reader.load_file_image(f"card_{card_number}.jpeg")
    card_reader()

    # logging.warning(re.sub("[^0-9A-Z]+", "", card_reader.text.upper()))
    card_reader.output_image(card_reader.found_card_image, f"test_image_{card_number}")


def all():
    for card_number in range(1, 9):
        run_card_read(card_number)


run_card_read("7_v2")
# all()
