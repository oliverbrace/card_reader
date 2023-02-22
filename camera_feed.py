import os

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import logging

import cv2

from card_finder import CardFinder
from image_functions.image_check import mean_squared_error
from match_card import MatchCard
from text_extraction import TextExtraction

logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(level=logging.DEBUG)
formatter = logging.Formatter("%(levelname)s : %(message)s")
console.setFormatter(formatter)
logger.addHandler(console)


def camera_feed():
    """Turn on camera and find card

    Raises:
        IOError: _description_
    """

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        c = cv2.waitKey(1)

        ret, original_frame = cap.read()
        original_frame = cv2.resize(
            original_frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA
        )
        card_reader = CardFinder()
        card_reader.load_image(original_frame)
        card_reader()
        if card_reader.found_card_image is not None:
            cv2.imshow("Input", card_reader.found_card_image)
            # card_reader.output_image(card_reader.card_image, "video_test")
            # break
            # card_reader.output_image(card_reader.found_card_image, f"video_test")
            textE = TextExtraction()
            textE.load_image(card_reader.card_image)
            textE()
            if textE.text is None:
                # logger.warning("No text found")
                continue

            logger.info(f"Text found: {textE.text}")

            if c == ord("a"):
                matchC = MatchCard(textE.text)
                matchC()
                if matchC.matched_card_name is None:
                    continue

                break

        else:
            cv2.imshow("Input", card_reader.canny_edge_image)

        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


camera_feed()
