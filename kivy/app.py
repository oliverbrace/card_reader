from camera_page import CameraPage
from display_page import DisplayPage
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from welcome_page import WelcomePage


class App(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        sm = MDScreenManager()

        welcome_page = WelcomePage(name="welcome_page")
        camera_page = CameraPage(name="camera_page")
        display_page = DisplayPage(name="display_page")

        sm.add_widget(welcome_page)
        sm.add_widget(camera_page)
        sm.add_widget(display_page)
        sm.current = "display_page"

        return sm


App().run()
