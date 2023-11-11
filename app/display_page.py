import pandas as pd
from common import PageBanner
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from style import table_colour


class DisplayPage(MDScreen):
    def __init__(self, **kwargs):
        super(DisplayPage, self).__init__(**kwargs)
        self.page_banner = PageBanner("Display Page", self.go_to_welcome_page)
        self.data_tables = MDDataTable(
            background_color_selected_cell=table_colour,
            check=True,
            column_data=[
                ("Name", dp(40), self.sort_on_col_1),
                ("Rarity", dp(30), self.sort_on_col_2),
                ("print_tag", dp(30)),
                ("1st Ed.", dp(30), self.sort_on_col_3),
                ("Dmged", dp(30), self.sort_on_col_4),
                ("Min Price", dp(25), self.sort_on_col_5),
                ("Avg Price", dp(25), self.sort_on_col_6),
                ("Max Price", dp(25), self.sort_on_col_7),
                ("Notes", dp(60)),
            ],
        )

        page_content = MDBoxLayout(orientation="vertical")
        page_content.add_widget(self.page_banner)
        page_content.add_widget(self.data_tables)
        self.add_widget(page_content)

    def go_to_welcome_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "welcome_page"

    def on_pre_enter(self):
        pd_cards = pd.read_csv("card_data.csv").fillna("")
        cards = list(pd_cards.itertuples(index=False, name=None))
        self.data_tables.row_data = cards  # Populate the MDDataTable

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
