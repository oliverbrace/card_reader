from common import BoxButton, CenteredLabel, GapLayout, InvisibleCard, PageBanner
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar


class WelcomePage(MDScreen):
    def go_to_new_card_page(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "new_card_page"

    def go_to_cards_page(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "cards_page"

    def on_pre_enter(self):
        welcome_bar = PageBanner("Welcome Page")

        # welcome_message = CenteredLabel(text=f"Hello world")

        go_to_cards_page_button = BoxButton(
            CenteredLabel(text="Current Cards"),
            # on_release=self.go_to_cards_page,
        )
        go_to_new_card_page_button = BoxButton(
            CenteredLabel(text="Add new Card"),
            # on_release=self.go_to_new_card_page,
        )

        self.add_widget(welcome_bar)

        page_content = GapLayout(
            [go_to_cards_page_button, go_to_new_card_page_button],
            offset=welcome_bar.height,
        )

        # page_content.add_widget(InvisibleCard())
        self.add_widget(page_content)
