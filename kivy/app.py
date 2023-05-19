from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from welcome_page import WelcomePage


class App(MDApp):
    def go_to_page_1(self, thing):
        self.root.transition.direction = "right"
        self.root.current = "page_1"

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        sm = MDScreenManager()

        welcome_page = WelcomePage(name="welcome_page")
        # p2 = Page2(name="page_2")

        sm.add_widget(welcome_page)
        # sm.add_widget(p2)

        return sm


App().run()
