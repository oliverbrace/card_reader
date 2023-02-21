import csv
import logging
import os
import re

from card_settings import (
    text_h_percentage,
    text_s_h_percentage,
    text_s_w_percentage,
    text_w_percentage,
)
from image_functions.clean_image import opening, sharpen
from image_functions.edge_detection import canny_edge_detection
from image_functions.serialize_image import ImageSerialize
from image_functions.transform_image import (
    create_grey,
    crop_image,
    grey_to_bl,
    invert_black_white,
)
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

        # De noise image
        # self.card_image = opening(self.card_image, 2)
        self.card_image = create_grey(self.card_image)
        # self.card_image = invert_black_white(self.card_image)
        # self.card_image = cv2.equalizeHist(self.card_image)
        # self.card_image = grey_to_bl(self.card_image, thresh=40)

        # self.card_image = crop_image(self.card_image, text_rectangle)
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        # self.card_image = clahe.apply(self.card_image)
        # self.card_image = cv2.adaptiveThreshold(
        #     self.card_image,
        #     255,
        #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #     cv2.THRESH_BINARY,
        #     21,
        #     20,
        # )
        # self.card_image = sharpen(self.card_image)
        # self.card_image = cv2.GaussianBlur(self.card_image, (5, 5), 0)

        self.text = find_text_in_image(self.card_image)
        print(self.text)
        # self.save_title_to_file()


def run(file):
    textE = TextExtraction()
    textE.load_file_image(file, path="images/extracted_cards")
    print(file)
    textE()
    file = file.split(".")[0]
    textE.output_image(textE.card_image, f"text_{file}", path="images/text_images")
    if textE.text is not None:
        logging.info(textE.text)


def all():
    files = os.listdir("images/extracted_cards")
    for file in files:
        run(file)


# all()
# run("video_test.png")
