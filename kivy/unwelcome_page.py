from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import M0DScreenManager

from kivy.uix.floatlayout import FloatLayout


class UnwelcomeWindow(MDScreen):
    def build(self):
        layout = FloatLayout()

        welcome_button = MDRectangleFlatButton(
            text="UNWelcome",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            on_release=self.welcome,
        )
        start_button = MDRectangleFlatButton(
            text="UNStart",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.start,
        )
        layout.add_widget(welcome_button)
        layout.add_widget(start_button)

        return layout

    def welcome(self, obj):
        print("Welcome to my application!")

    def start(self, obj):
        self.root.ids.content.text = "Let's get started!"
