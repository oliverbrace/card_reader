import os

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2

from card_reader import CardReader
from read_card.image_check import mean_squared_error

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    c = cv2.waitKey(1)

    ret, original_frame = cap.read()
    original_frame = cv2.resize(
        original_frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA
    )
    card_reader = CardReader()
    card_reader.load_image(original_frame)
    card_reader()
    frame = card_reader.card_image

    #! Keep rectangle on screen for more than a single frame
    cv2.imshow("Input", frame)
    if mean_squared_error(original_frame, frame):
        if c == ord("a"):
            card_reader.output_image(card_reader.card_image, f"video_test")

    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
