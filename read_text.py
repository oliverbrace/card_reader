import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"


def find_text_in_image(image):
    custom_config = r"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ- --psm 8"
    image = cv2.resize(image, None, fx=20, fy=20)
    return pytesseract.image_to_string(image, config=custom_config)
