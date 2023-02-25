import cv2

from image_functions.transform_image import create_grey


def get_contours(image):
    try:
        image = create_grey(image)
    except:
        pass

    contours, hierarchy = cv2.findContours(
        image=image, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE
    )
    return contours


def get_rectangle_size(rectangle):
    """_summary_

    Args:
        rectangle (tuple): xStart, yStart, width, height
    """
    return rectangle[2] * rectangle[3]


def get_rectangles(
    image,
    min_size=0,
    max_size=1000000,
    rect_min_width=15,
    rect_min_height=25,
    rect_max_width=100000,
    rect_max_height=100000,
):
    """_summary_

    Args:
        image

    Returns:
        _type_: List of [xStart, yStart, width, height]
    """
    contours = get_contours(image)
    rectangles = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > min_size and area < max_size:
            new_rect = cv2.boundingRect(c)
            if (
                new_rect[3] > rect_min_height
                and new_rect[2] > rect_min_width
                and new_rect[3] < rect_max_height
                and new_rect[2] < rect_max_width
            ):
                rectangles.append(new_rect)

    return rectangles


def find_biggest_rectangle(rectangles):
    """_summary_

    Args:
        rectangles List: [xStart, yStart, width, height]

    Returns:
        tuple: xStart, yStart, width, height
    """
    if not len(rectangles):
        raise Exception("No rectangles provided")

    biggest_rectangle_index = 0
    for index, rect in enumerate(rectangles):
        if index == 0:
            continue

        current_biggest = rectangles[biggest_rectangle_index]

        if get_rectangle_size(rect) > get_rectangle_size(current_biggest):
            biggest_rectangle_index = index

    return rectangles[biggest_rectangle_index]
