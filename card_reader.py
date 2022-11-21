import logging

import cv2
import numpy as np

from card_settings import (
    text_h_percentage,
    text_s_h_percentage,
    text_s_w_percentage,
    text_w_percentage,
)
from read_card.draw_rectangles import (
    draw_contours,
    draw_multiple_rectangles,
    draw_rectangle,
)
from read_card.extract_card import apply_mask, edge_mask, generate_mask
from read_card.find_rectangles import (
    find_biggest_rectangle,
    get_contours,
    get_rectangles,
)
from read_card.get_image import read_saved_image
from read_card.read_text import find_text_in_image
from read_card.transform_image import (
    create_grey,
    crop_image,
    grey_to_bl,
    invert_black_white,
)


class CardReader:
    def __init__(self, filename, search_method_colour=True):
        self.filename = filename
        self.original_image = None
        self.card_image = None
        self.search_method_colour = search_method_colour
        self.text = None

    def load_image(self):
        self.original_image = read_saved_image(
            self.filename, colour=self.search_method_colour
        )

    def extract_card_colour(self):
        mask = edge_mask(self.original_image)
        return apply_mask(self.original_image, mask)

    def extract_card_grey(self):
        # Not sure how to get to work
        (_, self.card_image) = cv2.threshold(
            self.card_image, 150, 255, cv2.THRESH_BINARY
        )

    def extract_card(self):
        if self.search_method_colour:
            border_image = self.extract_card_colour()
        else:
            self.extract_card_grey()

        rectangles = get_rectangles(border_image)
        rectangle = find_biggest_rectangle(rectangles)
        self.card_image = crop_image(self.original_image, rectangle)

    def clean_image(self):
        pass

    def output_card(self, file_name="test_image"):
        cv2.imwrite(
            f"temp_images/{file_name}.png",
            self.card_image,
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

    def find_draw_contours(self):
        cont = get_contours(self.card_image)
        self.card_image = draw_contours(self.original_image, cont)

    def __call__(self):
        self.load_image()
        self.extract_card()
        text_rectangle = self.find_text_rect()
        self.card_image = crop_image(self.card_image, text_rectangle)
        self.card_image = create_grey(self.card_image)
        self.text = find_text_in_image(self.card_image)


def run_card_read(card_number):
    card_reader = CardReader(f"card_{card_number}")
    card_reader()
    logging.warning(card_reader.text.replace(" ", "").strip())
    card_reader.output_card(f"test_image_{card_number}")


def all():
    for card_number in range(1, 9):
        run_card_read(card_number)


# run_card_read(1)
all()
