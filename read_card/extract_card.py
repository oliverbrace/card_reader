import cv2
import numpy as np
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
