from add_card_details_page import CardDetailsPage
from camera_page import CameraPage
from card_verification_page import VerifyCardPage
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
        verify_card_page = VerifyCardPage(name="verify_card_page")
        card_details_page = CardDetailsPage(name="card_details_page")

        sm.add_widget(welcome_page)
        sm.add_widget(camera_page)
        sm.add_widget(display_page)
        sm.add_widget(verify_card_page)
        sm.add_widget(card_details_page)
        sm.current = "camera_page"

        return sm


App().run()
