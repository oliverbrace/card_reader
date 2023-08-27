import os

from backend.camera_feed import preprocess_frame

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
from common import PageBanner
from kivy.uix.camera import Camera
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


class CameraPage(MDScreen):
    def __init__(self, **kwargs):
        super(CameraPage, self).__init__(**kwargs)
        self.camera = Camera(
            play=True,
            size_hint=(1, 1),
            keep_ratio=False,
            allow_stretch=True,
            height=100,
            width=100,
        )
        self.camera.bind(texture=self.on_frame)

    def go_to_process_card_page(self):
        self.manager.transition.direction = "left"
        self.manager.current = "verify_card_page"

    def go_to_welcome_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "welcome_page"

    def on_frame(self, instance, value):
        """Method to be executed for every frame"""
        # You can process the frame here
        preprocess_frame()

    def on_pre_enter(self):
        page_banner = PageBanner("Capture Page", self.go_to_welcome_page)

        page_content = MDBoxLayout(orientation="vertical")
        page_content.add_widget(page_banner)

        # Remove the camera from its current parent
        if self.camera.parent:
            self.camera.parent.remove_widget(self.camera)

        self.camera.play = True
        page_content.add_widget(self.camera)
        self.add_widget(page_content)

    def on_leave(self):
        self.camera.unbind(texture=self.on_frame)
        self.camera.play = False
