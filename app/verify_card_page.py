import cv2
from common import BoxButton, CenteredButtonsContainer, CenteredLabel, PageBanner
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


class VerifyCardPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the static UI components here
        self.page_banner = PageBanner("Verify Card page", self.go_to_camera_page)
        self.card_question_text = CenteredLabel(size_hint=(1, None))
        self.card_image = Image(allow_stretch=True, keep_ratio=True)
        correct_label = CenteredLabel(text="Correct")
        self.card_correct_button = BoxButton(
            correct_label, on_release=self.card_correct
        )
        incorrect_label = CenteredLabel(text="Incorrect")
        self.card_wrong_button = BoxButton(
            incorrect_label, on_release=self.card_incorrect
        )

        page_content = MDBoxLayout(orientation="vertical")
        page_content.add_widget(self.page_banner)
        page_content.add_widget(self.card_question_text)
        page_content.add_widget(self.card_image)
        buttons_container = CenteredButtonsContainer()
        buttons_container.add_widget(self.card_correct_button)
        buttons_container.add_widget(self.card_wrong_button)
        page_content.add_widget(buttons_container)

        self.add_widget(page_content)

    def go_to_card_details(self):
        self.manager.transition.direction = "left"
        self.manager.current = "card_details_page"

    def go_to_camera_page(self):
        self.manager.incorrect_guess = self.manager.current_card["name"]
        self.manager.current_card = None
        self.manager.transition.direction = "right"
        self.manager.current = "camera_page"

    def card_correct(self, _):
        self.go_to_card_details()

    def card_incorrect(self, _):
        self.go_to_camera_page()

    def on_pre_enter(self):
        if not hasattr(self.manager, "current_card"):
            card = {"name": "test", "image": Image(source="test_display_image.png")}

        card = self.manager.current_card

        # Update the card name directly
        self.card_question_text.text = f"Is the card called {card['name']}"

        # Update the card image directly
        self.card_image.texture = self.create_texture_from_frame(card["image"])

    @staticmethod
    def create_texture_from_frame(frame):
        """Create a Kivy texture from an RGB frame."""
        frame = cv2.flip(frame, 0)
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="rgb")
        texture.blit_buffer(frame.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
        return texture
