from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class CardApp(MDApp):
    def build(self):
        # Create the MDCard with FloatLayout as the layout
        card = MDCard(
            size_hint=(None, None),
            size=(300, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color="#648800",
        )
        card_layout = MDAnchorLayout(
            anchor_y="top",
            size_hint=(None, None),
            height=150,
            width=200,
            md_bg_color="#643800",
        )

        # Create the MDLabel
        label = MDLabel(
            text="Text at the top",
            halign="center",
            size_hint=(1, None),
            height=17,
            pos_hint={"top": 0},
        )
        label.md_bg_color = [1, 0.5, 0, 1]

        # Add the label to the card layout
        card_layout.add_widget(label)
        card.add_widget(card_layout)

        return card


CardApp().run()
