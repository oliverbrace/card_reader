import os

if False:
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
    from kivy.uix.camera import Camera

from common import BoxButton, CenteredLabel, PageBanner
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


class CameraPage(MDScreen):
    def __init__(self, **kwargs):
        super(CameraPage, self).__init__(**kwargs)
        if False:
            self.camera = Camera(
                play=True,
                size_hint=(1, 1),
                keep_ratio=False,
                allow_stretch=True,
                height=100,
                width=100,
            )
        else:
            self.camera = None

    def go_to_process_card_page(self):
        self.manager.transition.direction = "left"
        self.manager.current = "verify_card_page"

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
