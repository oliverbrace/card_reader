import csv
import logging
import re

import cv2
import numpy as np

from card_settings import card_height_width
from read_card.draw_rectangles import draw_rectangle, get_draw_contours
from read_card.extract_card import apply_mask, edge_mask, simple_edge_mask
from read_card.find_rectangles import (
    find_biggest_rectangle,
    get_contours,
    get_rectangles,
)
from read_card.get_image import find_text_rect, read_saved_image
from read_card.image_check import get_image_size, rectangle_shape_check
from read_card.read_text import find_text_in_image
from read_card.transform_image import create_grey, crop_image, invert_black_white


class CardReader:
    def __init__(self):
        self.original_image = None
        self.card_image = None
        self.text = None
        self.border_image = None
        self.image_height = None
        self.image_width = None

    def load_file_image(self, filename):
        self.original_image = read_saved_image(filename)
        self.image_height, self.image_width = get_image_size(self.original_image)
        logging.info("Loaded file image")

    def load_image(self, image):
        self.original_image = image
        self.image_height, self.image_width = get_image_size(self.original_image)
        logging.info("Loaded image")

    def output_image(self, image, file_name="test_image"):
        cv2.imwrite(
            f"temp_images/{file_name}.png",
            image,
        )

    def save_title_to_file(self):
        with open("unmatched_titles.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([re.sub("[^0-9A-Z-]+", "", self.text).upper()])

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
            self.card_image = draw_rectangle(self.original_image, rectangle)
        else:
            self.card_image = self.original_image

        # self.card_image = crop_image(self.original_image, rectangle)
        # text_rectangle = self.find_text_rect()
        # self.card_image = crop_image(self.card_image, text_rectangle)
        # self.card_image = create_grey(self.card_image)
        # self.text = find_text_in_image(self.card_image)
        # self.save_title_to_file()


def run_card_read(card_number):
    card_reader = CardReader()
    card_reader.load_file_image(f"card_{card_number}.jpeg")
    card_reader()

    # logging.warning(re.sub("[^0-9A-Z]+", "", card_reader.text.upper()))
    card_reader.output_image(card_reader.card_image, f"test_image_{card_number}")


def all():
    for card_number in range(1, 9):
        run_card_read(card_number)


run_card_read("7_v2")
# all()
