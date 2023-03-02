import os

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import logging

import cv2

from card_finder import CardFinder
from logger import Logger
from match_card import MatchCard
from preprocess_card_image import ImagePreprocessing
from text_extraction import TextExtraction

logger = Logger().load_logger()


def camera_feed():
    """Turn on camera and find card

    Raises:
        IOError: _description_
    """

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # i = 0
    while True:
        c = cv2.waitKey(1)
        if c == 27:
            break

        ret, original_frame = cap.read()
        original_frame = cv2.resize(
            original_frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA
        )

        image_preprocessing = ImagePreprocessing()
        image_preprocessing.load_image(original_frame)
        image_preprocessing()

        card_reader = CardFinder()
        card_reader.load_image(image_preprocessing.center_image)
        card_reader()
        if card_reader.found_card_image is None:
            cv2.imshow("Input", image_preprocessing.display_image)
            continue

        image_preprocessing.add_new_center_image(card_reader.found_card_image)
        cv2.imshow("Input", image_preprocessing.display_image)

        textE = TextExtraction()
        textE.load_image(card_reader.card_image)
        textE()
        if textE.text is None or textE.text == "":
            # logger.warning("No text found")
            continue

        # logger.info(f"Text found: {textE.text}")

        # if c == ord("a"):
        matchC = MatchCard(textE.text)
        matchC()
        if matchC.matched_card_name is None:
            continue

    cap.release()
    cv2.destroyAllWindows()


camera_feed()
