from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from kivy.uix.floatlayout import FloatLayout


class WelcomeScreen(MDScreen):
    def hello_world(self):
        print("Hello World!")


class WelcomeScreen2(MDScreen):
    def hello_world(self):
        print("Noooo World!")


class MyApp(MDApp):
    def build(self):
        sm = MDScreenManager()
        ws = WelcomeScreen(name="welcome")
        ws2 = WelcomeScreen2(name="unwelcome")

        sm.add_widget(ws)
        sm.add_widget(ws2)
        sm.current = "welcome"
        layout1 = FloatLayout()
        layout2 = FloatLayout()

        welcome_button = MDRectangleFlatButton(
            text="Welcome",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            # on_release=sm.switch_to(ws2, direction="left"),
        )
        start_button = MDRectangleFlatButton(
            text="Start",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            # on_release=sm.switch_to(ws),
        )
        layout1.add_widget(welcome_button)
        layout2.add_widget(start_button)

        ws.add_widget(layout1)
        ws2.add_widget(layout2)
        welcome_button.on_release = sm.switch_to(ws2, direction="left")
        start_button.on_release = sm.switch_to(ws, direction="right")

        return sm


if __name__ == "__main__":
    MyApp().run()
