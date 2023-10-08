import os

from backend.camera_feed import image_search

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
from common import PageBanner
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


class CameraPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = None
        self.texture = None
        self.image = None
        self.layout = MDBoxLayout(orientation="vertical")  # Initialize layout here
        self.clock_event = None
        self.incorrect_guesses = []

        # Add static components to the layout
        page_banner = PageBanner("Capture Page", self.go_to_welcome_page)
        self.layout.add_widget(page_banner)
        self.add_widget(self.layout)

    def go_to_verify_card_page(self, card):
        self.manager.current_card = card
        self.manager.transition.direction = "left"
        self.manager.current = "verify_card_page"

    def go_to_welcome_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "welcome_page"

    def on_pre_enter(self):
        self.init_capture_device()
        self.init_ui_elements()
        self.clock_event = Clock.schedule_interval(self.update, 0)
        if hasattr(self.manager, "incorrect_guess"):
            self.incorrect_guesses.append(self.manager.incorrect_guess)

    def on_leave(self):
        self.clock_event.cancel()
        self.capture.release()

    def init_capture_device(self):
        """Initialize the OpenCV video capture device."""
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Failed to open camera.")
            exit()

    def get_frame_from_capture(self):
        """Get a frame from the OpenCV video capture and convert it to RGB."""
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return ret, frame

    @staticmethod
    def create_texture_from_frame(frame):
        """Create a Kivy texture from an RGB frame."""
        frame = cv2.flip(frame, 0)
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="rgb")
        texture.blit_buffer(frame.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
        return texture

    def update_texture(self, frame):
        """Update the Kivy texture with a new RGB frame."""
        frame = cv2.flip(frame, 0)
        self.texture.blit_buffer(frame.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
        self.image.texture = self.texture

    def update(self, dt):
        """Main update loop."""
        ret, frame = self.get_frame_from_capture()
        card = image_search(frame, self.incorrect_guesses)
        if card:
            self.go_to_verify_card_page(card)

        if ret:
            self.update_texture(frame)
            self.layout.canvas.ask_update()

    def init_ui_elements(self):
        """Initialize the UI elements for the application."""
        if not self.image:
            ret, frame = self.get_frame_from_capture()
            self.texture = self.create_texture_from_frame(frame)
            self.image = Image(texture=self.texture, size_hint_y=0.9)
            self.layout.add_widget(self.image)
        else:
            # Don't readd ui elements
            ret, frame = self.get_frame_from_capture()
            self.update_texture(frame)
