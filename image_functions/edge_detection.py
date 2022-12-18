import logging

import cv2
import numpy as np
from scipy import ndimage
from skspatial.objects import Line, Sphere


def apply_mask(image, mask):
    return cv2.bitwise_and(image, image, mask=mask)


def find_lower_upper(center, distance):
    """Finds points of square

    Args:
        center (list): coordinates
        distance (float): distance to other points
    """
    sphere = Sphere(center, distance)
    line = Line([0, 0, 0], center)

    return sphere.intersect_line(line)


def edge_mask(image, border_colour, edge_method="HSV", distance=10):
    if edge_method == "HSV":
        points = find_lower_upper(border_colour, distance)
        lower, upper = bound_hsv(points)
        return generate_mask(image, cv2.COLOR_BGR2HSV, lower, upper)

    elif edge_method == "RGB":
        points = find_lower_upper(border_colour, distance)
        lower, upper = bound_255(points)
        return generate_mask(image, cv2.COLOR_BGR2RGB, lower, upper)

    elif edge_method == "LAB":
        points = find_lower_upper(border_colour, distance)
        lower, upper = bound_255(points)
        return generate_mask(image, cv2.COLOR_BGR2Lab, lower, upper)


def generate_mask(colour_image, conversion_code, lower, upper):
    """_summary_

    Args:
        colour_image (_type_): _description_

        if conversion_code cv2.COLOR_BGR2HSV
        H: 0-179, S: 0-255, V: 0-255.
        lower (np.array(list)): np.array([H, S, V])
        upper (np.array(list)): np.array([H, S, V])

        if conversion_code cv2.COLOR_BGR2RGB
        lower (np.array(list)): np.array([R, G, B])
        upper (np.array(list)): np.array([R, G, B])

        if conversion_code cv2.COLOR_BGR2Lab
        L: 0-255, a: 0-255, b: 0-255.
        lower (np.array(list)): np.array([L, a, b])
        upper (np.array(list)): np.array([L, a, b])

    """

    if lower is None or upper is None:
        raise Exception("Lower or Upper not set")

    converted = cv2.cvtColor(colour_image, conversion_code)
    mask = cv2.inRange(converted, lower, upper)
    return mask


def bound_255(points):
    # Bound values between 0 and 255
    for point in points:
        for index, colour in enumerate(point):
            if colour > 255:
                point[index] = 255
            elif colour < 0:
                point[index] = 0

    return points


def bound_hsv(points):
    for point in points:
        if point[0] > 179:
            point[0] = 179
        elif point[0] < 0:
            point[0] = 0

        for i in range(1, 3):
            if point[i] > 255:
                point[i] = 255
            elif point[i] < 0:
                point[i] = 0

    return points


def simple_edge_mask(image):
    # lower = np.array([150 / 2, 0, 0])
    # upper = np.array([360 / 2, 255, 255])

    lower = np.array([150 / 2, 18, 0])
    upper = np.array([360 / 2, 100, 200])

    return generate_mask(image, cv2.COLOR_BGR2HSV, lower, upper)


def edge_detection(img, v_operator, h_operator):
    # normalize the image
    img = img.astype("float64")
    img /= 255.0

    # convolve with v_operator and h_operator
    vertical = ndimage.convolve(img, v_operator)
    horizontal = ndimage.convolve(img, h_operator)

    # calculate the edged image
    edged_img = np.sqrt(np.square(horizontal) + np.square(vertical))
    edged_img *= 255

    return edged_img


def roberts_crossover(img):
    # setup the variables
    roberts_cross_v = np.array([[1, 0], [0, -1]])
    roberts_cross_h = np.array([[0, 1], [-1, 0]])
    return edge_detection(img, roberts_cross_v, roberts_cross_h)


def sobel_edge(img):
    # setup the variables
    sobel_v = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_h = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    return edge_detection(img, sobel_v, sobel_h)


def prewitt_edge(img):
    # setup the variables
    prewitt_v = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    prewitt_h = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    return edge_detection(img, prewitt_v, prewitt_h)


def canny_edge_detection(image, blur=7, threshold1=40, threshold2=100):
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except:
        logging.warning("Image may already be grey so skipping step")

    image = cv2.GaussianBlur(image, (blur, blur), 0)
    return cv2.Canny(image=image, threshold1=threshold1, threshold2=threshold2)
