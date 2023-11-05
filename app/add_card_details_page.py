from backend.add_info_db import CardRegisterAdder
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


class CardDetailsPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.damage_selected = False
        self.first_edition_selected = False

        layout = MDBoxLayout(orientation="vertical")

        page_banner = PageBanner(
            "Verify Card page", self.go_to_process_card_page, size_hint_y=None
        )

        self.rarity_container = TextWDropdown(
            "What is the rarity?",
            default="Common",
            on_release=self.rarity_select,
        )

        self.print_tag_container = TextWDropdown(
            "What is the print tag?",
            default="Not provided",
            on_release=self.printer_tag_select,
        )
        self.first_edition_container = TextWButtons(
            "Is your card first edition?", on_release=self.first_edition_select
        )
        self.damaged_container = TextWButtons(
            "Is your card damaged?", on_release=self.damage_select
        )
        self.notes_container = TextWTextField("Notes")
        self.done_button = BoxButton(
            CenteredLabel(text="Done"), disabled=True, on_release=self.confirm_card
        )
        scroll_view = MDScrollView()
        content = MDBoxLayout(orientation="vertical", size_hint_y=None)

        layout.add_widget(page_banner)
        layout.add_widget(scroll_view)
        scroll_view.add_widget(content)

        content.add_widget(self.rarity_container)
        content.add_widget(BlankSeparator())
        content.add_widget(self.print_tag_container)
        content.add_widget(BlankSeparator())
        content.add_widget(self.first_edition_container)
        content.add_widget(BlankSeparator())
        content.add_widget(self.damaged_container)
        content.add_widget(BlankSeparator())
        content.add_widget(self.notes_container)
        content.add_widget(BlankSeparator())
        content.add_widget(self.done_button)
        content.height = sum(child.height for child in content.children)

        self.add_widget(layout)

    def go_to_process_card_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "verify_card_page"

    def go_to_welcome_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "welcome_page"

    def finish_card_add(self):
        self.go_to_welcome_page()

    def set_card_adder_values(self):
        self.card_adder.get_card_prices()
        self.card_adder.first_edition = self.first_edition_container.answer
        self.card_adder.damaged = self.damaged_container.answer
        self.card_adder.notes = self.notes_container.notes_text_container.text

    def on_pre_enter(self):
        if hasattr(self.manager, "current_card"):
            self.card_adder = CardRegisterAdder(self.manager.current_card["name"])
        else:
            # For testing if card was not provided
            self.card_adder = CardRegisterAdder("Fusion Weapon")

        rarity_options = self.card_adder.possible_rarities + ["Other"]
        print_tag_options = ["Not provided"] + self.card_adder.possible_print_tags
        self.rarity_container.options = rarity_options
        self.print_tag_container.options = print_tag_options

        #! Should a method in it to reset
        self.rarity_container.dropdown = None
        self.print_tag_container.dropdown = None

        self.damage_selected = False
        self.first_edition_selected = False
        self.rarity_container.set_item("Common")
        self.print_tag_container.set_item("Not provided")
        self.first_edition_container.reset_buttons()
        self.damaged_container.reset_buttons()
        self.notes_container.clear_text()

    def rarity_select(self):
        self.card_adder.rarity = self.rarity_container.children[0].current_item

    def all_items_selected_check_wrapper(func):
        def wrapper(self):
            func(self)
            self.all_items_selected_check()

        return wrapper

    def all_items_selected_check(self):
        pass_checks = (
            self.damage_selected
            and self.first_edition_selected
            and self.card_adder.print_tag != "Not provided"
        )
        if pass_checks:
            self.done_button.disabled = False
        else:
            self.done_button.disabled = True

    @all_items_selected_check_wrapper
    def first_edition_select(self):
        self.first_edition_selected = True

    @all_items_selected_check_wrapper
    def damage_select(self):
        self.damage_selected = True

    @all_items_selected_check_wrapper
    def printer_tag_select(self):
        self.card_adder.print_tag = self.print_tag_container.children[0].current_item

    def confirm_card(self, _):
        self.set_card_adder_values()
        self.card_adder.write_card_to_csv()
        self.finish_card_add()
