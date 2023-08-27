"""
Load image in or get image from video stream
"""
import cv2


def read_saved_image(filename, colour=True, path="images/cards"):
    image = cv2.imread(
        path + "/" + filename,
        cv2.IMREAD_UNCHANGED if colour else cv2.IMREAD_GRAYSCALE,
    )

    if image is None:
        raise Exception("Image is blank. Check the path and filename")
    return image
