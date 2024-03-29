from kivy.metrics import dp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.widget import MDWidget
from style import border_colour, fill_colour, selected_color


class PageBanner(MDTopAppBar):
    def __init__(
        self,
        title,
        previous_page=None,
        download_list=None,
        delete_items=None,
        undo_delete=None,
        refresh_prices=None,
        edit_card_details=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        if previous_page:
            self.left_action_items = [["arrow-left", lambda x: previous_page()]]

        self.stored_r_actions = {}
        if download_list:
            self.stored_r_actions["download_button"] = [
                "file-download",
                lambda x: download_list(),
            ]

        if delete_items:
            self.stored_r_actions["delete_button"] = [
                "delete-forever",
                lambda x: delete_items(),
            ]

        if undo_delete:
            self.stored_r_actions["undo_button"] = [
                "undo-variant",
                lambda x: undo_delete(),
            ]

        if refresh_prices:
            self.stored_r_actions["refresh_button"] = [
                "database-refresh",
                lambda x: refresh_prices(),
            ]

        if edit_card_details:
            self.stored_r_actions["edit_button"] = [
                "pencil-box-outline",
                lambda x: edit_card_details(),
            ]

        if self.stored_r_actions != {}:
            self.current_r_actions = self.stored_r_actions.copy()
            self.right_action_items = self.trans(self.current_r_actions)

        self.title = title
        self.elevation = 4
        self.pos_hint = {"top": 1}
        self.height = 64

    def hide_item(self, action_button):
        try:
            self.current_r_actions.pop(action_button)
        except KeyError:
            return

        self.right_action_items = self.trans(self.current_r_actions)

    def show_item(self, action_button):
        if action_button in self.current_r_actions:
            return

        try:
            delete_action = self.stored_r_actions[action_button]
            self.current_r_actions[action_button] = delete_action
        except KeyError:
            return

        self.right_action_items = self.trans(self.current_r_actions)

    def add_back_button(self, back_function):
        "for loading back button after init"
        self.left_action_items = [["arrow-left", lambda x: back_function()]]

    def hide_delete(self):
        self.hide_item("delete_button")

    def show_delete(self):
        self.show_item("delete_button")

    def hide_undo(self):
        self.hide_item("undo_button")

    def show_undo(self):
        self.show_item("undo_button")

    def hide_refresh(self):
        self.hide_item("refresh_button")

    def show_refresh(self):
        self.show_item("refresh_button")

    def hide_edit(self):
        self.hide_item("edit_button")

    def show_edit(self):
        self.show_item("edit_button")

    @staticmethod
    def trans(input_dict):
        return list(input_dict.values())


class CenteredLabel(MDLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.halign = "center"


class SmallLabel(CenteredLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint_y = None
        self.height = 17


class LargeLabel(CenteredLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint_y = None
        self.font_style = "H4"


class TopCenteredContainer(MDAnchorLayout):
    """Container will be centered and contents put at top"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos_hint = {"center_x": 0.5}
        self.anchor_y = "top"
        self.size_hint_y = None
        self.height = 50


class BoxButton(MDCard):
    """Button to click on that can take other objects"""

    def __init__(self, *args, disabled=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint = (None, None)
        self.size = ("200dp", "100dp")
        self.halign = "center"
        self.pos_hint = {"center_x": 0.5}
        self.style = "outlined"
        self.line_width = 2
        self.disabled = disabled
        self.line_color = border_colour
        self.md_bg_color = fill_colour


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


class BlankSeparator(MDWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint_y = None
        self.height = 50


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

            if gap_height < 10:
                gap_height = 10

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


class FillSpace(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HelpBox(MDBoxLayout):
    """Is a box layout that is white"""

    def __init__(self, *args, **kwargs):
        self.md_bg_color = [1, 1, 1, 1]


class TextWButtons(MDBoxLayout):
    def __init__(self, text, on_release=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.size_hint = (1, None)
        self.height = 150
        self.on_release = on_release

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
        self.set_yes()
        self.on_release()

    def set_yes(self):
        self.children[0].children[1].md_bg_color = selected_color
        self.children[0].children[0].md_bg_color = fill_colour
        self.answer = True

    def clicked_no(self, _):
        self.set_no()
        self.on_release()

    def set_no(self):
        self.children[0].children[1].md_bg_color = fill_colour
        self.children[0].children[0].md_bg_color = selected_color
        self.answer = False

    def reset_buttons(self):
        self.children[0].children[1].md_bg_color = fill_colour
        self.children[0].children[0].md_bg_color = fill_colour
        self.answer = None

    def set_answer(self, answer):
        if answer:
            self.set_yes()
        else:
            self.set_no()


class TextWDropdown(MDBoxLayout):
    def __init__(self, text, on_release, options=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        # This height is actually 83 for some reason
        # 100 gives a slight space above the object which is nice when its the first object
        self.height = 100

        self.options = options
        self.dropdown = None
        self.on_release = on_release

        text_container = TopCenteredContainer(
            SmallLabel(text=text),
        )
        rarity_dropdown_button = MDDropDownItem(pos_hint={"center_x": 0.5})
        rarity_dropdown_button.bind(on_release=self.show_dropdown)

        self.add_widget(text_container)
        self.add_widget(rarity_dropdown_button)

    def show_dropdown(self, dropdown_item):
        if self.dropdown is None:
            dropdown_items = [
                {
                    "viewclass": "OneLineListItem",
                    "text": rarity,
                    "height": 54,
                    "on_release": lambda x=rarity: self.dropdown_item_clicked(x),
                }
                for rarity in self.options
            ]
            self.dropdown = MDDropdownMenu(
                caller=dropdown_item,
                items=dropdown_items,
                width_mult=4,
            )
        self.dropdown.open()

    def set_item(self, x):
        self.children[0].set_item(x)

    def dropdown_item_clicked(self, x):
        self.set_item(x)
        self.dropdown.dismiss()
        self.on_release()


class TextWTextField(MDBoxLayout):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.size_hint = (0.8, None)
        self.height = 117

        self.pos_hint = {"center_x": 0.5}

        text_container = TopCenteredContainer(
            SmallLabel(text=text),
        )

        # Can't change size. Defaults to 100
        self.notes_text_container = MDTextField()

        self.add_widget(text_container)
        self.add_widget(self.notes_text_container)

    def clear_text(self):
        self.notes_text_container.text = ""


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


class LoadingIcon(MDSpinner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint = (None, None)
        self.size = (dp(30), dp(30))
        self.pos_hint = ({"center_x": 0.5, "center_y": 0.5},)
