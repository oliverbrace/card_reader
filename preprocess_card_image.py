import logging
import os

from card_settings import card_ratio
from image_functions.draw_rectangles import darken_outside_rectangle
from image_functions.edge_detection import canny_edge_detection
from image_functions.serialize_image import ImageSerialize
from image_functions.transform_image import (
    crop_image,
    gray_add_colour_dimension,
    paste_image,
)


class ImagePreprocessing(ImageSerialize):
    """Cleans the image before finding the rectangle"""

    def __init__(self):
        # image_height, image_width and original_image
        super().__init__()

        # Images
        self.center_image = None
        self.dimmed_image = None
        self.canny_edge_image = None
        self.display_image = None

    def create_canny_edge_image(self):
        if self.center_image is None:
            raise Exception("No canny_edge image")

        canny_edge_image = canny_edge_detection(self.center_image, blur=7)
        return gray_add_colour_dimension(canny_edge_image)

    def find_center_rectangle(self):
        """Creates a rectangle that shares the same center and height as the
            original image but has the same ratio as a card

        Returns:
            List: Rectangle that has same height as original image
                but width that is proportional to a card_ratio
        """
        height = self.image_height
        estimated_width = height / card_ratio
        width_start_point = int(self.image_width / 2 - estimated_width / 2)
        return [width_start_point, 0, int(estimated_width), height]

    def paste_canny_into_dimmed(self, center_rectangle):
        """Paste the canny_edge_image into the
        dimmed_image so that they have the same center point

        Args:
            center_rectangle (List): (xStart, yStart, width, height)

        """
        return paste_image(
            self.dimmed_image,
            self.canny_edge_image,
            center_rectangle[0],
            center_rectangle[1],
        )

    def __call__(self):
        center_rectangle = self.find_center_rectangle()
        self.center_image = crop_image(self.original_image, center_rectangle)
        self.canny_edge_image = self.create_canny_edge_image()

        # This is just so that it looks good when displayed to screen.
        self.dimmed_image = darken_outside_rectangle(
            self.original_image, center_rectangle
        )

        self.display_image = self.paste_canny_into_dimmed()
