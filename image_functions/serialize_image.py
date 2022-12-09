import logging

import cv2

from image_functions.get_image import read_saved_image
from image_functions.image_check import get_image_size


class ImageSerialize:
    def __init__(self):
        self.original_image = None
        self.image_height = None
        self.image_width = None

    def load_file_image(self, filename, path="images/cards/"):
        self.original_image = read_saved_image(filename, path=path)
        self.image_height, self.image_width = get_image_size(self.original_image)
        logging.info("Loaded file image")

    def load_image(self, image):
        self.original_image = image
        self.image_height, self.image_width = get_image_size(self.original_image)
        logging.info("Loaded image")

    def output_image(self, image, file_name="test_image", path="images/temp_images"):
        if image is None:
            raise Exception("No image provided")

        cv2.imwrite(
            f"{path}/{file_name}.png",
            image,
        )