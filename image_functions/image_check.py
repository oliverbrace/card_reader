import cv2
import numpy as np


def num_channels_check(img):
    return img.ndim


def get_image_size(image):
    """_summary_

    Args:
        image (_type_): _description_

    Returns:
        _type_: height, width
    """
    image_shape = image.shape
    return image_shape[0], image_shape[1]


def get_pixel_count(image):
    height, width = get_image_size(image)
    return height * width


def rectangle_shape_check(rectangle, margin_of_error=0.15):
    """Checks if image has roughly correct dimensions

    Args:
        rectangle (List): (xStart, yStart, width, height)
        margin_of_error (float, optional): margin_of_error. Defaults to 0.15.

    Raises:
        Exception: if margin_of_error is less than 0

    Returns:
        Bool: Is correct size check
    """
    if margin_of_error < 0:
        raise Exception("margin_of_error must be greater than 0")

    _, _, width, height = rectangle
    image_height_width_ratio = height / width
    return (
        height_width_ratio * (1 + margin_of_error) > image_height_width_ratio
        and height_width_ratio * (1 - margin_of_error) < image_height_width_ratio
    )


def mean_squared_error(img1, img2):
    h, w, _ = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err / (float(h * w))
    return mse


def percentage_black_pixels(image):
    """_summary_

    Args:
        image (_type_):
    """
    return percentage_colour_pixels(image, 0)


def percentage_white_pixels(image):
    """_summary_

    Args:
        image (_type_):
    """
    return percentage_colour_pixels(image, 255)


def percentage_colour_pixels(image, colour):
    """_summary_

    Args:
        image (_type_): image
        colour (int): _description_

    Returns:
        _type_: _description_
    """
    return np.sum(image == colour) / get_pixel_count(image)
