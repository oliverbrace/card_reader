import os

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

from common import BoxButton, CenteredLabel, GapLayout, PageBanner
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen

from kivy.uix.camera import Camera


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

    def go_to_process_card_page(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "new_card_page"

    def go_to_welcome_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "welcome_page"

    def process_image(self, _):
        processed_image = True
        if processed_image:
            # Found text in image
            self.go_to_process_card_page()
        else:
            # Fail message
            pass

    def on_pre_enter(self):
        page_banner = PageBanner("Capture Page", self.go_to_welcome_page)
        go_to_process_card_page_button = BoxButton(
            CenteredLabel(text="Capture"),
            on_release=self.process_image,
        )

        page_content = MDBoxLayout(orientation="vertical")
        page_content.add_widget(page_banner)

        # Remove the camera from its current parent
        if self.camera.parent:
            self.camera.parent.remove_widget(self.camera)

        self.camera.play = True
        page_content.add_widget(self.camera)
        page_content.add_widget(go_to_process_card_page_button)
        self.add_widget(page_content)

    def on_leave(self):
        self.camera.play = False