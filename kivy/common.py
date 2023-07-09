from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from style import border_colour, fill_colour, selected_color


class PageBanner(MDTopAppBar):
    def __init__(self, title, previous_page=None):
        super().__init__()
        if previous_page:
            self.left_action_items = [["arrow-left", lambda x: previous_page()]]

        self.title = title
        self.elevation = 4
        self.pos_hint = {"top": 1}
        self.height = 64


class CenteredLabel(MDLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.halign = "center"


class SmallLabel(CenteredLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint_y = None
        self.height = "17dp"


class TopCenteredContainer(MDAnchorLayout):
    """Container will be centered and contents put at top"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos_hint = {"center_x": 0.5}
        self.anchor_y = "top"
        self.size_hint = (None, None)
        self.size = ("200dp", "50dp")


class BoxButton(MDCard):
    """Button to click on that can take other objects"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint = (None, None)
        self.size = ("200dp", "100dp")
        self.halign = "center"
        self.pos_hint = {"center_x": 0.5}
        self.style = "outlined"
        self.line_color = border_colour
        self.md_bg_color = fill_colour
        self.line_width = 2


class SmallContainer(MDBoxLayout):
    """The Container will match the
    size of the objects placed inside of it"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adaptive_size = True


class InvisibleCard(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint = (None, None)
        self.opacity = 0


class GapLayout(MDBoxLayout):
    def __init__(self, widgets, offset=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        gap_height = 0

        widgets_height = 0
        for widget in widgets:
            widgets_height += widget.height
            if hasattr(widget, "spacing"):
                widgets_height += widget.spacing

        def update_gap_height(instance, value):
            nonlocal gap_height
            available_height = self.height - widgets_height - offset
            gap_height = available_height / (
                len(widgets) + 1
            )  # Divide by the number of gaps (3 cards = 2 gaps)
            update_layout()

        def update_layout():
            self.clear_widgets()
            for widget in widgets:
                self.add_widget(widget)

                # Add the gap between cards
                gap = MDBoxLayout(size_hint=(1, None), height=gap_height)
                self.add_widget(gap)

        self.bind(size=update_gap_height)

        update_gap_height(self, self.size)


class CenteredButtonsContainer_OLD(MDAnchorLayout):
    """Passed in button will be centered"""

    def __init__(self, buttons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anchor_x = "center"
        self.size_hint = (1, None)

        small_container = SmallContainer(orientation="horizontal")
        for button in buttons:
            small_container.add_widget(button)

        self.add_widget(small_container)


class CenteredButtonsContainer(MDBoxLayout):
    """Passed in button will be centered"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "horizontal"
        self.adaptive_width = True
        self.pos_hint = {"center_x": 0.5}


class HelpBox(MDBoxLayout):
    """Is a box layout that is white"""

    def __init__(self, *args, **kwargs):
        self.md_bg_color = [1, 1, 1, 1]


class TextWButtons(MDBoxLayout):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.size_hint = (1, None)
        self.height = 150

        self.answer = None

        text_container = TopCenteredContainer(SmallLabel(text=text))

        yes_button = BoxButton(
            CenteredLabel(text="Yes"),
            on_release=self.clicked_yes,
        )
        no_button = BoxButton(
            CenteredLabel(text="No"),
            on_release=self.clicked_no,
        )
        button_container = CenteredButtonsContainer()
        button_container.add_widget(yes_button)
        button_container.add_widget(no_button)
        self.add_widget(text_container)
        self.add_widget(button_container)

    def clicked_yes(self, _):
        self.children[0].children[1].md_bg_color = selected_color
        self.children[0].children[0].md_bg_color = fill_colour
        self.answer = True

    def clicked_no(self, _):
        self.children[0].children[1].md_bg_color = fill_colour
        self.children[0].children[0].md_bg_color = selected_color
        self.answer = False


class TextWDropdown(MDBoxLayout):
    def __init__(self, text, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.adaptive_height = True
        self.spacing = 40

        self.dropdown = None

        centered_text = SmallLabel(text=text)
        rarity_dropdown_button = MDDropDownItem(
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        rarity_dropdown_button.text = "Common"
        rarity_dropdown_button.bind(on_release=self.show_dropdown)

        self.add_widget(centered_text)
        self.add_widget(rarity_dropdown_button)

    def show_dropdown(self, dropdown_item):
        if self.dropdown is None:
            dropdown_items = [
                {
                    "viewclass": "OneLineListItem",
                    "text": f"Item {i}",
                    "height": 54,
                    "on_release": lambda x=f"Item {i}": self.dropdown_item_selected(x),
                }
                for i in range(1, 4)
            ]
            self.dropdown = MDDropdownMenu(
                caller=dropdown_item,
                items=dropdown_items,
                width_mult=4,
            )
        self.dropdown.open()

    def dropdown_item_selected(self, x):
        self.children[0].set_item(x)
        self.dropdown.dismiss()


class TextWTextField(MDBoxLayout):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.adaptive_height = True
        self.spacing = 40

        self.pos_hint = {"center_x": 0.5}
        self.size_hint = (0.8, 1)

        centered_text = CenteredLabel(text=f"Notes", size_hint=(1, None))
        notes_text = MDTextField(multiline=True)

        self.add_widget(centered_text)
        self.add_widget(notes_text)


class TwoButtons(CenteredButtonsContainer):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        yes_button = BoxButton(
            CenteredLabel(text="Yes"),
            on_release=self.clicked_yes,
        )
        no_button = BoxButton(
            CenteredLabel(text="No"),
            on_release=self.clicked_no,
        )

        self.add_widget(yes_button)
        self.add_widget(no_button)

    def clicked_yes(self, _):
        self.children[0].children[1].md_bg_color = selected_color
        self.children[0].children[0].md_bg_color = fill_colour
        self.answer = True

    def clicked_no(self, _):
        self.children[0].children[1].md_bg_color = fill_colour
        self.children[0].children[0].md_bg_color = selected_color
        self.answer = False
