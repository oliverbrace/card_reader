import cv2
import numpy as np

from draw_rectangles import draw_contours, draw_multiple_rectangles, draw_rectangle
from extract_card import apply_mask, edge_mask
from find_rectangles import find_biggest_rectangle, get_contours, get_rectangles
from get_image import read_saved_image


class CardReader:
    def __init__(self, filename, search_method_colour=True):
        self.filename = filename
        self.original_image = None
        self.image = None
        self.search_method_colour = True

    def load_image(self):
        self.original_image = read_saved_image(
            self.filename, colour=self.search_method_colour
        )
        self.image = self.original_image

    def extract_card_colour(self):
        mask = edge_mask(self.image)
        self.image = apply_mask(self.image, mask)

    def extract_card_gray(self):
        # Not sure how to get to work
        (_, self.image) = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)

    def extract_card(self):
        if self.search_method_colour:
            self.extract_card_colour()
        else:
            self.extract_card_gray()

    def clean_image(self):
        pass

    def output_card(self):
        cv2.imwrite(
            "temp_images/test_image.png",
            self.image,
        )

    def __call__(self):
        self.load_image()
        self.extract_card()
        rectangles = get_rectangles(self.image, min_size=3000)
        rectangle = find_biggest_rectangle(rectangles)
        self.image = draw_rectangle(self.original_image, rectangle, thickness=10)

        self.output_card()


card_reader = CardReader("card_8")
card_reader()
