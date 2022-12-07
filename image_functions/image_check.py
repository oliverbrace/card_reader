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


def rectangle_shape_check(rectangle, height_width_ratio, margin_of_error=0.1):
    """
    Checks if image has roughly correct dimensions
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
