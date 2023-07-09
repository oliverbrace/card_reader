from common import (
    BoxButton,
    CenteredButtonsContainer,
    CenteredLabel,
    GapLayout,
    HelpBox,
    PageBanner,
    TextWButtons,
    TextWDropdown,
    TextWTextField,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield.textfield import MDTextField

from kivy.properties import StringProperty


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class CardDetailsPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_to_process_card_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "verify_card_page"

    def go_to_welcome_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "welcome_page"

    def finish_card_add(self):
        self.go_to_welcome_page()

    def set_item(self, text_item):
        self.screen.ids.drop_item.set_item(text_item)
        self.menu.dismiss()

    def notes(self):
        notes_container = MDBoxLayout(
            orientation="vertical",
            size_hint=(0.8, 1),
            pos_hint={"center_x": 0.5},
        )
        notes_question = CenteredLabel(text=f"Notes", size_hint=(1, None))
        notes_text = MDTextField(multiline=True)
        notes_container.add_widget(notes_question)
        notes_container.add_widget(notes_text)
        return notes_container

    def on_pre_enter(self):
        page_banner = PageBanner("Verify Card page", self.go_to_process_card_page)

        rarity_container = TextWDropdown("What is the rarity of your card?", options=[])

        first_edition_container = TextWButtons("Is your card first edition?")

        damaged_container = TextWButtons("Is your card damaged?")

        notes_container = TextWTextField("Notes")

        done_button = BoxButton(
            CenteredLabel(text="Yes"),
            # on_release=self.done_button_action,
        )

        self.add_widget(page_banner)
        page_content = GapLayout(
            [first_edition_container, damaged_container],
            offset=page_banner.height,
        )

        # self.add_widget(rarity_container)
        # self.add_widget(first_edition_container)
        # self.add_widget(damaged_container)
        # self.add_widget(notes_container)
        # page_content.add_widget(done_button)

        self.add_widget(page_content)
