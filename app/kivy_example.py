from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen


class Example(MDApp):
    def build(self):
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("No.", dp(30), self.sort_col_1),
                ("Team Lead", dp(30), self.sort_col_2),
            ],
            row_data=[
                ("1", "Chase Nguyen"),
                ("2", "Brie Furman"),
                ("3", "Jeremy lake"),
                ("4", "Angelica Howards"),
                ("5", "Diane Okuma"),
            ],
            elevation=2,
        )
        screen = MDScreen()
        screen.add_widget(self.data_tables)
        return screen

    def sort_col_1(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][0]))

    def sort_col_2(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][1]))


Example().run()
