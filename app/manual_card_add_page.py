import difflib

import pandas as pd
from common import (
    BlankSeparator,
    BoxButton,
    CenteredButtonsContainer,
    CenteredLabel,
    FillSpace,
    PageBanner,
    TextWTextField,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


class ManualCardAddPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the static UI components here
        self.page_banner = PageBanner("Manual card add", self.go_to_welcome_page)
        self.card_name_input = TextWTextField("What is your card called?")
        self.card_name_input.notes_text_container.bind(text=self.card_input_change)
        page_content = MDBoxLayout(orientation="vertical")
        page_content.add_widget(self.page_banner)
        page_content.add_widget(BlankSeparator())
        page_content.add_widget(self.card_name_input)
        self.buttons = MDBoxLayout(orientation="vertical")

        page_content.add_widget(self.buttons)
        self.add_widget(page_content)

    def go_to_card_details(self):
        self.manager.transition.direction = "left"
        self.manager.current = "card_details_page"

    def go_to_welcome_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "welcome_page"

    def picked_card(self, box_object):
        self.manager.current_card = {"name": box_object.children[0].text}
        self.manager.card_added_page = "manual"
        self.go_to_card_details()

    def on_pre_enter(self):
        self.manager.current_card = None
        self.card_name_input.clear_text()

    def card_input_change(self, event, text):
        card_names = self.get_similar_names(text)
        if self.buttons.children != []:
            buttons = list(self.buttons.children)
            for child in buttons:
                self.buttons.remove_widget(child)
        for name in card_names:
            card_label = CenteredLabel(text=name)
            card_button = BoxButton(card_label, on_release=self.picked_card)
            self.buttons.add_widget(card_button)

    @staticmethod
    def get_similar_names(card_input):
        if not card_input:
            return []

        cards_df = pd.read_csv("all_cards.csv")
        transformed_card_names = cards_df["Transformed Name"]
        matches = difflib.get_close_matches(card_input, transformed_card_names, n=3)
        return matches
