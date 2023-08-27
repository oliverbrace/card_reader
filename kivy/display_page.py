import pandas as pd
from common import BoxButton, CenteredLabel, PageBanner
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from style import table_colour

from kivy.metrics import dp


class DisplayPage(MDScreen):
    def go_to_welcome_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "welcome_page"

    def on_pre_enter(self):
        page_banner = PageBanner("Display Page", self.go_to_welcome_page)
        pd_cards = pd.read_csv("card_data.csv")
        cards = list(pd_cards.itertuples(index=False, name=None))
        data_tables = MDDataTable(
            background_color_selected_cell=table_colour,
            check=True,
            column_data=[
                ("Name", dp(40), self.sort_on_col_1),
                ("Rarity", dp(30), self.sort_on_col_2),
                ("1st Ed.", dp(50), self.sort_on_col_3),
                ("Damaged", dp(30), self.sort_on_col_4),
                ("Avg Price", dp(30), self.sort_on_col_5),
                ("Max Price", dp(30), self.sort_on_col_6),
                ("Min Price", dp(30), self.sort_on_col_7),
            ],
            row_data=cards,
        )
        data_tables.bind(on_row_press=self.on_row_press)
        page_content = MDBoxLayout(orientation="vertical")
        page_content.add_widget(page_banner)
        page_content.add_widget(data_tables)
        self.add_widget(page_content)

    def sort_on_col_1(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][1]))

    def sort_on_col_2(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][1]))

    def sort_on_col_3(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][3]))

    def sort_on_col_4(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][3]))

    def sort_on_col_5(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][4]))

    def sort_on_col_6(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][5]))

    def sort_on_col_7(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][6]))

    def on_row_press(self, instance_table, instance_row):
        """Called when a table row is clicked."""

        print(instance_table, instance_row)