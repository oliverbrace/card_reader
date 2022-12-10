import cv2
import numpy as np

from image_functions.find_rectangles import get_contours
from image_functions.image_check import get_image_size


def draw_contours(image, contours):
    return cv2.drawContours(
        image=image, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2
    )


def get_draw_contours(contour_image, draw_image):
    contours = get_contours(contour_image)
    return draw_contours(draw_image, contours)


def draw_rectangle(image, rectangle, colour=(0, 255, 0), thickness=-1):
    """_summary_

    Args:
        rect (_type_): list with [xStart, yStart, width, height]
        image (_type_): Colour image to draw on
        colour (tuple):
    """
    image_copy = image.copy()

    xStart = int(rectangle[0])
    xEnd = int((rectangle[0] + rectangle[2]))
    yStart = int(rectangle[1])
    yEnd = int((rectangle[1] + rectangle[3]))

    return cv2.rectangle(image_copy, (xStart, yStart), (xEnd, yEnd), colour, thickness)


def draw_multiple_rectangles(image, rectangles, thickness=2):
    """_summary_

    Args:
        image (_type_): Colour image to be drawn on

    Returns:
        _type_: _description_
    """

    image_rect = image
    for rect in rectangles:
        image_rect = draw_rectangle(
            image_rect, rect, colour=(0, 255, 0), thickness=thickness
        )

    return image_rect


def darken_outside_rectangle(image, rectangle):
    """Will darken everything outside of provided rectangle

    Args:
        image (_type_): image where you want to darken
        rectangle (_type_): [xStart, yStart, width, height]

    Returns:
        _type_: _description_
    """

    # Get image size
    height, width = get_image_size(image)

    # Create a new image and with previous image dimensions
    blank_image = np.zeros((height, width))

    # Create a rectangle with the desired dimensions
    rectangle_image = draw_rectangle(blank_image, rectangle, colour=(255, 255, 255))

    # Make everything outside the rectangle darker
    image[rectangle_image == 0] = 0.5 * image[rectangle_image == 0]

    return image
