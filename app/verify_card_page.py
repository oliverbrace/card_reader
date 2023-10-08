import cv2
from common import BoxButton, CenteredButtonsContainer, CenteredLabel, PageBanner
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


class VerifyCardPage(MDScreen):
    def go_to_card_details(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "card_details_page"

    def go_to_camera_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "camera_page"

    def card_correct(self, _):
        self.go_to_card_details("")

    def card_incorrect(self, _):
        self.go_to_camera_page()

    def on_pre_enter(self):
        page_banner = PageBanner("Verify Card page", self.go_to_camera_page)
        card_correct_button = BoxButton(
            CenteredLabel(text="Correct"),
            on_release=self.card_correct,
        )
        card_wrong_button = BoxButton(
            CenteredLabel(text="Incorrect"),
            on_release=self.card_incorrect,
        )

        card = self.manager.current_card

        card_name = card.name
        card_question_text = CenteredLabel(
            text=f"Is the card called {card_name}", size_hint=(1, None)
        )
        card_image = Image(texture=self.create_texture_from_frame(card.image))

        # Set the image size to fill the parent widget
        card_image.allow_stretch = True
        card_image.keep_ratio = True

        page_content = MDBoxLayout(orientation="vertical")
        page_content.add_widget(page_banner)
        page_content.add_widget(card_question_text)
        page_content.add_widget(card_image)
        buttons_container = CenteredButtonsContainer()
        buttons_container.add_widget(card_correct_button)
        buttons_container.add_widget(card_wrong_button)
        page_content.add_widget(buttons_container)
        self.add_widget(page_content)

    @staticmethod
    def create_texture_from_frame(frame):
        """Create a Kivy texture from an RGB frame."""
        frame = cv2.flip(frame, 0)
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="rgb")
        texture.blit_buffer(frame.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
        return texture
