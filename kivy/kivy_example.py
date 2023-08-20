from common import BlankSeparator, TextWButtons
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView

from kivy.uix.widget import Widget


class MainApp(MDApp):
    def build(self):
        layout = MDBoxLayout(orientation="vertical")

        top_space = Widget(
            size_hint_y=None, height=150
        )  # This is a blank widget that takes up the first 150px from the top
        layout.add_widget(top_space)

        scrollview = MDScrollView(md_bg_color=[1, 0.5, 1, 1])
        scroll_list = MDBoxLayout(
            orientation="vertical", size_hint_y=None, height=50 * 300
        )
        for i in range(50):  # Populating the list with 50 items
            scroll_list.add_widget(BlankSeparator())
            item = TextWButtons(text=f"Item {i}")
            scroll_list.add_widget(item)

        scrollview.add_widget(scroll_list)
        layout.add_widget(scrollview)

        return layout


MainApp().run()
