from common import (
    BlankSeparator,
    BoxButton,
    CenteredLabel,
    PageBanner,
    TextWButtons,
    TextWDropdown,
    TextWTextField,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield.textfield import MDTextField


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
        layout = MDBoxLayout(orientation="vertical")

        page_banner = PageBanner(
            "Verify Card page", self.go_to_process_card_page, size_hint_y=None
        )

        rarity_container = TextWDropdown("What is the rarity of your card?", options=[])

        first_edition_container = TextWButtons("Is your card first edition?")

        damaged_container = TextWButtons("Is your card damaged?")

        notes_container = TextWTextField("Notes")

        done_button = BoxButton(
            CenteredLabel(text="Yes"),
            # on_release=self.done_button_action,
        )

        layout.add_widget(page_banner)
        scroll_view = MDScrollView()

        content = MDBoxLayout(orientation="vertical", size_hint_y=None)

        content.add_widget(rarity_container)
        content.add_widget(BlankSeparator())
        content.add_widget(first_edition_container)
        content.add_widget(BlankSeparator())
        content.add_widget(damaged_container)
        content.add_widget(BlankSeparator())
        content.add_widget(notes_container)
        content.add_widget(BlankSeparator())
        content.add_widget(done_button)

        content.height = sum(child.height for child in content.children)

        scroll_view.add_widget(content)

        layout.add_widget(scroll_view)
        self.add_widget(layout)
