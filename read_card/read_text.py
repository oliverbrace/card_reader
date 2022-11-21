import logging

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"


def find_text_in_image(image, psm=7):
    custom_config = (
        f"-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm {psm}"
    )
    # Increase image size which improves detection of individual letters
    image = cv2.resize(image, None, fx=2, fy=2)
    try:
        text = pytesseract.image_to_string(image, config=custom_config)
    except:
        logging.warning("pytesseract Failed")
        text = None

    return text
