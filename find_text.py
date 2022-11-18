import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"


def find_text_in_image(image):
    custom_config = r"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8"
    return pytesseract.image_to_string(image, config=custom_config)
