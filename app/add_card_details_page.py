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
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from style import table_colour


class CardDetailsPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.damage_selected = False
        self.first_edition_selected = False

        layout = MDBoxLayout(orientation="vertical")

        self.page_banner = PageBanner("Verify Card page", size_hint_y=None)

        self.scroll_view = MDScrollView()
        content = MDBoxLayout(orientation="vertical", size_hint_y=None)

        layout.add_widget(self.page_banner)
        layout.add_widget(self.scroll_view)
        self.scroll_view.add_widget(content)

        self.create_widgets()

        content.add_widget(self.rarity_container)
        content.add_widget(BlankSeparator())
        content.add_widget(self.print_tag_container)
        content.add_widget(BlankSeparator())
        content.add_widget(self.price_table)
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

    def go_to_manual_card_add_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "manual_card_add_page"

    def go_to_display_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "display_page"

    def go_to_welcome_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "welcome_page"

    def finish_card_add(self):
        if self.manager.card_added_page == "edit":
            self.go_to_display_page()
        else:
            self.go_to_welcome_page()

    def set_card_adder_values(self):
        self.card_adder.first_edition = self.first_edition_container.answer
        self.card_adder.damaged = self.damaged_container.answer
        self.card_adder.notes = self.notes_container.notes_text_container.text

    def create_widgets(self):
        self.rarity_container = TextWDropdown(
            "What is the rarity?",
            on_release=self.rarity_select,
        )

        self.print_tag_container = TextWDropdown(
            "What is the print tag?",
            on_release=self.printer_tag_select,
        )

        self.price_table = MDDataTable(
            background_color_selected_cell=table_colour,
            check=False,
            column_data=[
                ("Exact Match", dp(41)),
                ("Avg Price", dp(26)),
                ("Max Price", dp(26)),
                ("Min Price", dp(26)),
            ],
            height=120,
            size_hint=(0.8, None),
            pos_hint={"center_x": 0.5},
        )

        self.first_edition_container = TextWButtons(
            "Is your card first edition?", on_release=self.first_edition_select
        )
        self.damaged_container = TextWButtons(
            "Is your card damaged?", on_release=self.damage_select
        )
        self.notes_container = TextWTextField("Notes")

        self.price_table.row_data = [("-", "-", "-", "-")]
        self.done_button = BoxButton(
            CenteredLabel(text="Done"), disabled=True, on_release=self.confirm_card
        )

    def on_pre_enter(self):
        if hasattr(self.manager, "current_card"):
            self.card_adder = CardRegisterAdder(self.manager.current_card["name"])
        else:
            # For testing if card was not provided
            self.card_adder = CardRegisterAdder("Fusion Weapon")

        if self.manager.card_added_page == "manual":
            back_function = self.go_to_manual_card_add_page
        elif self.manager.card_added_page == "edit":
            back_function = self.go_to_display_page
        else:
            back_function = self.go_to_process_card_page
        self.page_banner.add_back_button(back_function)

        rarity_options = self.card_adder.possible_rarities + ["Other"]
        print_tag_options = ["Not provided"] + self.card_adder.possible_print_tags
        self.rarity_container.options = rarity_options
        self.print_tag_container.options = print_tag_options

        self.rarity_container.dropdown = None
        self.print_tag_container.dropdown = None

        if self.manager.card_added_page == "edit":
            self.edit_card_set_up()
        else:
            self.damage_selected = False
            self.first_edition_selected = False
            self.rarity_container.set_item("Common")
            self.print_tag_container.set_item("Not provided")
            self.price_table.row_data = [("-", "-", "-", "-")]
            self.first_edition_container.reset_buttons()
            self.damaged_container.reset_buttons()
            self.notes_container.clear_text()
        self.scroll_view.scroll_to(self.rarity_container, animate=False)

    def edit_card_set_up(self):
        self.damage_selected = True
        self.first_edition_selected = True
        rarity = self.manager.current_card["rarity"]
        print_tag = self.manager.current_card["print_tag"]
        first_edition = self.manager.current_card["first_edition"]
        damaged = self.manager.current_card["damaged"]
        notes = self.manager.current_card["notes"]
        self.card_adder.rarity = rarity
        self.card_adder.print_tag = print_tag
        self.card_adder.rarity = rarity
        self.card_adder.first_edition = first_edition
        self.card_adder.damaged = damaged
        self.card_adder.notes = notes
        self.rarity_container.set_item(rarity)
        self.print_tag_container.set_item(print_tag)
        self.first_edition_container.set_answer(first_edition)
        self.damaged_container.set_answer(damaged)
        self.notes_container.notes_text_container.text = notes
        self.update_price_display()

    def update_price_display(self):
        if self.print_tag_container.children[0].current_item == "Not provided":
            self.price_table.row_data = [("-", "-", "-", "-")]
            return

        self.card_adder.get_card_prices()
        self.price_table.row_data = [
            (
                self.card_adder.match_type,
                self.card_adder.lowest_card_price,
                self.card_adder.average_card_price,
                self.card_adder.highest_card_price,
            )
        ]

    def rarity_select(self):
        self.card_adder.rarity = self.rarity_container.children[0].current_item
        self.update_price_display()

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
        self.update_price_display()

    def confirm_card(self, _):
        self.set_card_adder_values()
        if self.manager.card_added_page == "edit":
            index = self.manager.current_card["index"]
            self.card_adder.edit_card(index)
        else:
            self.card_adder.write_card_to_csv()
        self.finish_card_add()
