import os
import time

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.togglebutton import ToggleButton


class CameraClick(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.camera = Camera(resolution=(640, 480), play=False)
        self.add_widget(self.camera)

        play_button = ToggleButton(text="Play", size_hint_y=None, height="48dp")
        play_button.bind(on_press=self.toggle_camera)
        self.add_widget(play_button)

        capture_button = Button(text="Capture", size_hint_y=None, height="48dp")
        capture_button.bind(on_press=self.capture)
        self.add_widget(capture_button)

    def toggle_camera(self, instance):
        self.camera.play = not self.camera.play

    def capture(self, instance):
        """
        Function to capture the images and give them the names
        according to their captured time and date.
        """
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png(f"IMG_{timestr}.png")
        print("Captured")


class TestCamera(App):
    def build(self):
        return CameraClick()


TestCamera().run()
