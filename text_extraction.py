import csv
import logging
import re

from card_settings import (
    text_h_percentage,
    text_s_h_percentage,
    text_s_w_percentage,
    text_w_percentage,
)
from image_functions.serialize_image import ImageSerialize
from image_functions.transform_image import create_grey, crop_image
from read_text import find_text_in_image


class TextExtraction(ImageSerialize):
    """Extracts the text from Card Image"""

    def __init__(self):
        self.card_image = None
        self.card_text = None

    def save_title_to_file(self):
        with open("unmatched_titles.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([re.sub("[^0-9A-Z-]+", "", self.text).upper()])

    def find_text_rect(self):
        # Assumes height is roughly correct
        rectangle = []
        height = self.original_image.shape[0]
        rectangle.append(height * text_s_w_percentage)
        rectangle.append(height * text_s_h_percentage)
        rectangle.append(height * text_w_percentage)
        rectangle.append(height * text_h_percentage)
        rectangle = tuple(rectangle)
        return rectangle

    def __call__(self):
        if self.original_image is None:
            logging.error("No image has been loaded in")
            return

        text_rectangle = self.find_text_rect()
        self.card_image = crop_image(self.original_image, text_rectangle)
        self.card_image = create_grey(self.card_image)

        self.text = find_text_in_image(self.card_image)
        # self.save_title_to_file()


def run(card_number):
    textE = TextExtraction()
    textE.load_file_image(f"test_image_{card_number}.png", path="temp_images/")
    textE()
    textE.output_image(textE.card_image, f"test_image_{card_number}")


def all():
    for card_number in range(1, 9):
        run(card_number)


# all()
# run(1)
