import csv
import os
import re

from card_settings import (
    text_h_percentage,
    text_s_h_percentage,
    text_s_w_percentage,
    text_w_percentage,
)
from image_functions.clean_image import closing, opening, sharpen
from image_functions.edge_detection import canny_edge_detection
from image_functions.serialize_image import ImageSerialize
from image_functions.transform_image import (
    create_grey,
    crop_image,
    grey_to_bl,
    invert_black_white,
)
from logger import Logger
from read_text import find_text_in_image

logger = Logger().load_logger()


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
        """_summary_

        Returns:
            List: (xStart, yStart, width, height)
        """

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
            logger.error("No image has been loaded in")
            return

        text_rectangle = self.find_text_rect()
        self.card_image = crop_image(self.original_image, text_rectangle)
        self.card_image = create_grey(self.card_image)
        self.text = find_text_in_image(self.card_image, psm=7)
        # De noise image
        # self.card_image = opening(self.card_image, 2)
        # self.card_image = create_grey(self.card_image)
        # self.card_image = invert_black_white(self.card_image)
        # self.card_image = cv2.equalizeHist(self.card_image)
        # self.card_image = grey_to_bl(self.card_image, thresh=40)

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

        # self.text = find_text_in_image(self.card_image, psm=8)
        # self.save_title_to_file()


def run(file, path="images/extracted_cards"):
    textE1 = TextExtraction()
    textE1.load_file_image(file, path=path)
    textE1()

    textE1.card_image = create_grey(textE1.card_image)
    # textE1.card_image = closing(textE1.card_image, 3)
    textE1.card_image = invert_black_white(textE1.card_image)
    textE1.text = find_text_in_image(textE1.card_image, psm=7)

    textE2 = TextExtraction()
    textE2.load_file_image(file, path=path)
    textE2()

    textE2.card_image = invert_black_white(textE2.card_image)
    textE2.card_image = create_grey(textE2.card_image)
    textE2.text = find_text_in_image(textE2.card_image, psm=7)
    logger.info(f"One {textE1.text}")
    logger.info(f"Two {textE2.text}")


def all():
    path = "images/video_extract"
    files = os.listdir(path)
    for file in files:
        run(file, path=path)


# all()
# run("video_test.png")
