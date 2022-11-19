import cv2
import numpy as np

from draw_rectangles import draw_contours, draw_multiple_rectangles, draw_rectangle
from extract_card import apply_mask, edge_mask
from find_rectangles import find_biggest_rectangle, get_contours, get_rectangles
from get_image import read_saved_image
from read_text import find_text_in_image
from transform_image import crop_image

card_height = 8.6
text_height_start = 0.4
text_start_percentage_card_height = text_height_start / card_height
text_height_end = 1.2
text_end_percentage_card_height = text_height_start / card_height
text_height = text_height_end - text_height_start
text_percentage_card_height = text_height / card_height


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

    def output_card(self, file_name="test_image"):
        cv2.imwrite(
            f"temp_images/{file_name}.png",
            self.image,
        )

    @staticmethod
    def find_text_rect(rectangle):
        rectangle = list(rectangle)
        rectangle[1] = rectangle[1] + rectangle[3] * (text_start_percentage_card_height)
        rectangle[3] = rectangle[3] * text_percentage_card_height
        rectangle = tuple(rectangle)
        return rectangle

    def find_draw_contours(self):
        cont = get_contours(self.image)
        self.image = draw_contours(self.original_image, cont)

    def __call__(self):
        self.load_image()
        self.extract_card()
        rectangles = get_rectangles(self.image)
        rectangle = find_biggest_rectangle(rectangles)
        # self.image = draw_rectangle(self.original_image, rectangle, thickness=10)

        text_rectangle = self.find_text_rect(rectangle)
        self.image = crop_image(self.original_image, text_rectangle)

        a = find_text_in_image(self.image)


card_reader = CardReader("card_1")
card_reader()
card_reader.output_card("test_image_1")


def all():
    for i in range(1, 9):
        card_reader = CardReader(f"card_{i}")
        card_reader()
        card_reader.output_card(f"test_image_{i}")
