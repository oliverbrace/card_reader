from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

from kivy.metrics import dp


class GapLayout(MDBoxLayout):
    def __init__(self, widgets, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        gap_height = 0

        widgets_height = 0
        for widget in widgets:
            widgets_height += widget.height

        def update_gap_height(instance, value):
            nonlocal gap_height
            available_height = self.height - widgets_height
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


class TestApp(MDApp):
    def build(self):
        card1 = MDCard(
            size_hint=(None, None),
            height=dp(10),
            width=dp(10),
            md_bg_color=[0, 0, 0, 1],
        )
        card2 = MDCard(size_hint=(1, None), height=dp(20), md_bg_color=[0, 0, 0, 1])
        card3 = MDCard(size_hint=(1, None), height=dp(30), md_bg_color=[0, 0, 0, 1])
        card4 = MDCard(size_hint=(1, None), height=dp(40), md_bg_color=[0, 0, 0, 1])

        root = GapLayout([card1, card2, card3, card4])
        return root


# Run the app
TestApp().run()
