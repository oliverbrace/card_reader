import cv2


def draw_contours(image, contours):
    return cv2.drawContours(
        image=image, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2
    )


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
