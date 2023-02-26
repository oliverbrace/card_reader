import logging
import os

from image_functions.draw_rectangles import draw_rectangle
from image_functions.edge_detection import canny_edge_detection
from image_functions.find_rectangles import find_biggest_rectangle, get_rectangles
from image_functions.image_check import rectangle_shape_check
from image_functions.serialize_image import ImageSerialize
from image_functions.transform_image import crop_image, gray_add_colour_dimension


class CardFinder(ImageSerialize):
    """Finds the Card in an Image"""

    def __init__(self, is_original_canny=False):
        # image_height, image_width and original_image
        super().__init__()

        self.is_original_canny = is_original_canny
        self.canny_edge_image = None
        self.found_card_image = None
        self.card_image = None

    def create_canny_edge_image(self):
        canny_edge_image = canny_edge_detection(self.original_image, blur=7)
        return gray_add_colour_dimension(canny_edge_image)

    def find_card(self):
        rectangles = get_rectangles(
            self.canny_edge_image,
            rect_min_height=self.image_height * 0.4,
            # rect_min_width=self.image_width * 0.4,
            rect_max_height=self.image_height * 0.9,
            rect_max_width=self.image_width * 0.9,
        )
        if len(rectangles) == 0:
            # logging.warning("no rectangle")
            return None

        # Check each rectangle has same ratio as card ratio
        possible_rectangles = []
        for rectangle in rectangles:
            if rectangle_shape_check(rectangle):
                possible_rectangles.append(rectangle)

        if len(possible_rectangles) == 0:
            return None

        return find_biggest_rectangle(possible_rectangles)

    def __call__(self):
        if self.original_image is None:
            raise Exception("No image provided")

        if self.is_original_canny:
            self.canny_edge_image = self.original_image
        else:
            self.canny_edge_image = self.create_canny_edge_image()

        rectangle = self.find_card()

        if rectangle is not None:
            self.found_card_image = draw_rectangle(
                self.canny_edge_image, rectangle, thickness=1
            )

            self.card_image = crop_image(self.original_image, rectangle)


def run_card_read(file):
    card_reader = CardFinder()
    card_reader.load_file_image(file)
    card_reader()
    # file = file.split(".")[0]
    card_reader.output_image(card_reader.card_image, f"MY_NEW_THING")


def all():
    files = os.listdir("images/cards")
    for file in files:
        run_card_read(file)


# run_card_read("card_1.jpeg")
# all()
