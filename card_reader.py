import cv2

from get_image import read_saved_image


class CardReader:
    def __init__(self, filename):
        self.filename = filename
        self.image = None

    def get_image(self):
        self.image = read_saved_image(self.filename)

    def output_image(self):
        cv2.imwrite("temp_images/test_image.png", self.image)

    def __call__(self):
        self.get_image()
        self.output_image()


card_reader = CardReader("card_1")
card_reader()
