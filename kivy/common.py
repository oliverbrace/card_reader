from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from style import border_colour, fill_colour


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
        # self.size_hint_y = None #023A80.


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

        def update_gap_height(instance, value):
            nonlocal gap_height
            available_height = self.height - widgets_height - offset
            gap_height = available_height / (
                len(widgets) + 1
            )  # Divide by the number of gaps (3 cards + 2 gaps)
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


class HelpBox(MDBoxLayout):
    """Is a box layout that is white"""

    def __init__(self, *args, **kwargs):
        self.md_bg_color = [1, 1, 1, 1]
