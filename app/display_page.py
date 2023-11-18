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
        self.checked_rows = []
        self.deleting = False
        self.page_banner = PageBanner(
            "Display Page",
            self.go_to_welcome_page,
            self.download_file,
            self.delete_select_rows,
            self.undo_delete_action,
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

    def update_data_table(self):
        pd_cards = pd.read_csv("card_data.csv").reset_index().fillna("")
        cards = self.table_format(pd_cards)
        self.data_table.row_data = cards  # Populate the MDDataTable

    def update_summary_table(self):
        pd_cards = pd.read_csv("card_data.csv").reset_index().fillna("")
        if len(pd_cards) == 0:
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
        self.update_data_table()
        self.uncheck_all_boxes()
        self.page_banner.hide_delete()
        self.page_banner.hide_undo()
        self.update_summary_table()

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
        data_to_delete = self.checked_rows
        self.delete_data(data_to_delete)
        self.page_banner.show_undo()

        # Re populate data table
        self.update_data_table()
        # Uncheck all boxes
        self.uncheck_all_boxes()
        # Hide delete icon
        self.page_banner.hide_delete()
        # Rec populate summary table
        self.update_summary_table()

    def uncheck_all_boxes(self):
        self.checked_rows = []

        # Without this this will trigger check_button_pressed code
        self.deleting = True
        self.data_table.table_data.select_all("normal")
        self.deleting = False

    def check_button_pressed(self, instance_table, current_row):
        if not self.deleting:
            self.update_checks(instance_table)
            self.delete_icon_check()

    def delete_icon_check(self):
        if self.checked_rows == []:
            self.page_banner.hide_delete()
        else:
            self.page_banner.show_delete()

    @staticmethod
    def delete_data(data_to_delete):
        pd_cards = pd.read_csv("card_data.csv").reset_index().fillna("")
        # So users can undo a delete
        pd_cards.drop("index", axis=1).to_csv("card_data_pre_delete.csv", index=False)
        rows_to_delete = pd.DataFrame(data_to_delete, columns=pd_cards.columns)["index"]

        # Modify existing csv and upload new one without deleted rows
        new_csv = pd_cards[~pd_cards["index"].isin(rows_to_delete)]
        new_csv.drop("index", inplace=True, axis=1)
        new_csv.to_csv("card_data.csv", index=False)

    def update_checks(self, instance_table):
        # WARNING: get_row_checks not reliable
        #  see https://github.com/kivymd/KivyMD/issues/924
        #  see https://github.com/kivymd/KivyMD/issues/1123
        self.checked_rows = []
        table_data = instance_table.table_data
        for page, selected_cells in table_data.current_selection_check.items():
            for column_index in selected_cells:
                data_index = int(
                    page * table_data.rows_num
                    + column_index / table_data.total_col_headings
                )
                self.checked_rows.append(list(table_data.row_data[data_index]))

    def undo_delete_action(self):
        self.undo_delete()
        self.update_summary_table()
        self.update_data_table()

    def undo_delete(self):
        # Switch card_data_pre_delete with card_data
        old_pd_cards = pd.read_csv("card_data_pre_delete.csv").fillna("")
        current_pd_cards = pd.read_csv("card_data.csv").fillna("")

        old_pd_cards.to_csv("card_data.csv", index=False)
        current_pd_cards.to_csv("card_data_pre_delete.csv", index=False)
