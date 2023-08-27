import os

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import logging

import cv2
from backend.add_info_db import CardRegisterAdder
from backend.card_finder import CardFinder
from backend.logger import Logger
from backend.match_card import MatchCard
from backend.preprocess_card_image import ImagePreprocessing
from backend.text_extraction import TextExtraction

logger = Logger().load_logger()


def card_check(card_name):
    query = f"Is {card_name} your card? (Y/N)"

    while True:
        response = input(query).upper()
        if response == "Y":
            return True
        elif response == "N":
            return False
        else:
            print("Please put either Y or N")


def open_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    return cap


def get_frame_from_camera(cap):
    ret, original_frame = cap.read()
    # Can be used to resize the image if desired
    original_frame = cv2.resize(
        original_frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA
    )
    return original_frame


def preprocess_frame(frame):
    image_preprocessing = ImagePreprocessing()
    image_preprocessing.load_image(frame)
    image_preprocessing()
    return image_preprocessing


def find_card_in_frame(image_preprocessing):
    card_reader = CardFinder()
    card_reader.load_image(image_preprocessing.center_image)
    card_reader()
    return card_reader


def extract_text_from_card(card_reader):
    textE = TextExtraction()
    textE.load_image(card_reader.card_image)
    textE()
    return textE.text


def match_card_from_text(text):
    matchC = MatchCard(text)
    matchC()
    return matchC.matched_card_name


def register_card(card_name):
    card_adder = CardRegisterAdder(card_name)
    card_adder()


def camera_feed():
    cap = open_camera()

    # i = 0  # This was commented out in your code
    attempted_cards = []
    while True:
        c = cv2.waitKey(1)
        if c == 27:
            break

        original_frame = get_frame_from_camera(cap)
        image_preprocessing = preprocess_frame(original_frame)

        card_reader = find_card_in_frame(image_preprocessing)
        if card_reader.found_card_image is None:
            cv2.imshow("Input", image_preprocessing.display_image)
            continue

        image_preprocessing.add_new_center_image(card_reader.found_card_image)
        cv2.imshow("Input", image_preprocessing.display_image)

        text = extract_text_from_card(card_reader)
        if not text:
            # logger.warning("No text found")
            continue

        # logger.info(f"Text found: {text}")

        matched_card_name = match_card_from_text(text)
        if not matched_card_name or matched_card_name in attempted_cards:
            continue

        found_card = card_check(matched_card_name)
        if not found_card:
            attempted_cards.append(matched_card_name)
            continue

        return matched_card_name

        # register_card(matched_card_name)
        break

    cap.release()
    cv2.destroyAllWindows()


# camera_feed()
