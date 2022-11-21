import cv2
import numpy as np


def generate_mask(colour_image, lower, upper):
    """_summary_

    Args:
        colour_image (_type_): _description_

        H: 0-179, S: 0-255, V: 0-255.
        lower (np.array(list)): np.array([H, S, V])
        upper (np.array(list)): np.array([H, S, V])

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    if lower is None or upper is None:
        raise Exception("Lower or Upper not set")

    hsv = cv2.cvtColor(colour_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    return mask


def apply_mask(image, mask):
    return cv2.bitwise_and(image, image, mask=mask)


def edge_mask(image):
    lower = np.array([150 / 2, 18, 0])
    upper = np.array([360 / 2, 100, 200])
    return generate_mask(image, lower, upper)
