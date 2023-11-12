import pandas as pd
from backend.misc import open_with_default_app
from common import PageBanner
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from style import table_colour


class DisplayPage(MDScreen):
    def __init__(self, **kwargs):
        super(DisplayPage, self).__init__(**kwargs)
        self.page_banner = PageBanner(
            "Display Page",
            self.go_to_welcome_page,
            self.download_file,
            self.delete_select_rows,
        )
        self.summary_table = MDDataTable(
            background_color_selected_cell=table_colour,
            check=False,
            height=120,
            size_hint=(1, None),
            column_data=[
                ("Total Cards", dp(18)),
                ("Uq Cards", dp(15)),
                ("Total 1st Ed", dp(18)),
                ("Total Min Price", dp(30)),
                ("Total Avg Price", dp(35)),
                ("Total Max Price", dp(35)),
            ],
        )

        self.data_table = MDDataTable(
            background_color_selected_cell=table_colour,
            check=True,
            use_pagination=True,
            # Not possible to sort first column
            column_data=[
                ("No.", dp(20)),
                ("Name", dp(40), self.sort_name),
                ("Rarity", dp(30), self.sort_rarity),
                ("print_tag", dp(30)),
                ("1st Ed.", dp(30), self.sort_1st_ed),
                ("Dmged", dp(30), self.sort_dmged),
                ("Min Price", dp(25), self.sort_min_price),
                ("Avg Price", dp(25), self.sort_avg_price),
                ("Max Price", dp(25), self.sort_max_price),
                ("Notes", dp(60)),
            ],
        )
        self.data_table.bind(on_check_press=self.check_button_pressed)

        page_content = MDBoxLayout(orientation="vertical")
        page_content.add_widget(self.page_banner)
        page_content.add_widget(self.summary_table)
        page_content.add_widget(self.data_table)
        self.add_widget(page_content)

    def go_to_welcome_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "welcome_page"

    @staticmethod
    def string_prices_to_numbers(prices):
        """Takes a series of string numbers and returns a dataframe of those numbers

        Returns:
            _type_: _description_
        """
        split_prices = prices.str.split("-", expand=True)
        if len(split_prices.columns) == 1:
            split_prices[1] = split_prices[0]
        else:
            split_prices[1] = split_prices[1].fillna(split_prices[0])
        split_prices[0] = pd.to_numeric(split_prices[0].str.replace("£", ""))
        split_prices[1] = pd.to_numeric(split_prices[1].str.replace("£", ""))
        return split_prices

    def calculate_total_price(self, prices):
        """_summary_

        Args:
            prices (pd.Series): series of prices of cards. Can either be a
                number or range like "x-y"
        """
        split_prices = self.string_prices_to_numbers(prices)
        low_total = split_prices[0].sum()
        high_total = split_prices[1].sum()

        if low_total == high_total:
            return f"£{split_prices[0].sum():.2f}"

        return f"£{split_prices[0].sum():.2f}-£{split_prices[1].sum():.2f}"

    @staticmethod
    def table_format(data):
        """Put pandas data in format for table

        Args:
            data (pd.DataFrame): data to be turned into put into a table

        Returns:
            _type_: _description_
        """
        return list(data.itertuples(index=False, name=None))

    def on_pre_enter(self):
        pd_cards = pd.read_csv("card_data.csv").reset_index().fillna("")
        cards = self.table_format(pd_cards)
        self.data_table.row_data = cards  # Populate the MDDataTable
        self.delete_icon_check(self.data_table)
        if len(cards) == 0:
            self.summary_table.row_data = [("-", "-", "-", "-", "-", "-")]
        else:
            self.summary_table.row_data = [
                (
                    len(pd_cards),
                    len(pd.unique(pd_cards["card_name"])),
                    pd_cards["first_edition"].sum(),
                    self.calculate_total_price(pd_cards["lowest_card_price"]),
                    self.calculate_total_price(pd_cards["average_card_price"]),
                    self.calculate_total_price(pd_cards["highest_card_price"]),
                )
            ]

    def sort_name(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][1]))

    def sort_rarity(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][2]))

    def sort_1st_ed(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][4]))

    def sort_dmged(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][5]))

    def sort_min_price(self, data):
        return self.money_value_sort(data, 6, True)

    def sort_avg_price(self, data):
        return self.money_value_sort(data, 7)

    def sort_max_price(self, data):
        return self.money_value_sort(data, 8)

    def money_value_sort(self, data, column, lower_num=False):
        """_summary_

        Args:
            data (tuple): data that will be sorted
            column (int): number to be sorted
            lower_num (bool, optional): If True will use the lower value in a range
                ele will use the higher number. Defaults to False.

        Returns:
            _type_: _description_
        """
        pd_data = pd.DataFrame(data)
        prices = self.string_prices_to_numbers(pd_data[column])
        range_column = 0 if lower_num else 1
        new_index = prices.sort_values(by=range_column).index
        pd_data = pd_data.loc[new_index]
        tuple(new_index)
        data = self.table_format(pd_data)
        return [tuple(new_index), tuple(data)]

    def download_file(self):
        open_with_default_app("card_data.csv")

    def on_row_press(self, instance_table, instance_row):
        """Called when a table row is clicked."""

        print(instance_table, instance_row)

    def delete_select_rows(self):
        self.data_table.get_row_checks()

    def check_button_pressed(self, instance_table, current_row):
        self.delete_icon_check(instance_table)

    def delete_icon_check(self, table):
        if table.get_row_checks() == []:
            self.page_banner.hide_delete()
        else:
            self.page_banner.show_delete()
