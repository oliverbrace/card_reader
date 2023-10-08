import os

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import datetime

import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager


class CameraScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = None
        self.texture = None
        self.image = None
        self.timestamp_label = None
        self.layout = BoxLayout(orientation="vertical")
        self.add_widget(self.layout)

    def on_enter(self):
        """Called when the screen is fully entered and displayed."""
        self.init_capture_device()
        self.init_ui_elements()
        # Schedule the update function to run as frequently as possible
        Clock.schedule_interval(self.update, 0)

    def init_capture_device(self):
        """Initialize the OpenCV video capture device."""
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Failed to open camera.")
            exit()

        ret, frame = self.capture.read()
        if ret:
            print(f"Frame shape: {frame.shape}")  # Print frame shape
        else:
            print("Failed to grab frame from camera.")

    def init_ui_elements(self):
        """Initialize the UI elements for the application."""
        ret, frame = self.get_frame_from_capture()
        if ret:
            self.texture = self.create_texture_from_frame(frame)
            # Create Image widget for Kivy to display the texture
            self.image = Image(texture=self.texture, size_hint_y=0.9)
            self.layout.add_widget(self.image)
            # A label to display the timestamp
            self.timestamp_label = MDLabel(size_hint_y=0.1, font_size=20)
            self.layout.add_widget(self.timestamp_label)
        else:
            print("Failed to get frame for UI initialization.")

    def get_frame_from_capture(self):
        """Get a frame from the OpenCV video capture and convert it to RGB."""
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 0)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return ret, frame

    def create_texture_from_frame(self, frame):
        """Create a Kivy texture from an RGB frame."""
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="rgb")
        texture.blit_buffer(frame.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
        return texture

    def update_texture(self, frame):
        """Update the Kivy texture with a new RGB frame."""
        self.texture.blit_buffer(frame.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
        self.image.texture = self.texture

    def update(self, dt):
        """Main update loop."""
        ret, frame = self.get_frame_from_capture()
        if ret:
            self.update_texture(frame)
            self.update_timestamp()

    def update_timestamp(self):
        """Update the timestamp displayed in the label."""
        current_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
        self.timestamp_label.text = f"Updated at: {current_time}"

    def on_stop(self):
        """Close the video capture when the application stops."""
        self.capture.release()


class CameraApp(MDApp):
    def build(self):
        sm = MDScreenManager()
        cs = CameraScreen(name="camera_page")
        sm.add_widget(cs)
        sm.current = "camera_page"
        return sm


if __name__ == "__main__":
    CameraApp().run()
