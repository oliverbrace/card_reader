from common import BoxButton, CenteredLabel, GapLayout, PageBanner
from kivymd.uix.screen import MDScreen


class WelcomePage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        page_banner = PageBanner("Welcome Page")

        go_to_display_page_button = BoxButton(
            CenteredLabel(text="Current Cards"),
            on_release=self.go_to_display_page,
        )
        go_to_camera_page_button = BoxButton(
            CenteredLabel(text="Add new Card"),
            on_release=self.go_to_camera_page,
        )
        go_to_manual_card_page_button = BoxButton(
            CenteredLabel(text="Manually add new Card"),
            on_release=self.go_to_manual_card_page,
        )

        self.add_widget(page_banner)

        page_content = GapLayout(
            [
                go_to_display_page_button,
                go_to_camera_page_button,
                go_to_manual_card_page_button,
            ],
            offset=page_banner.height,
        )

        self.add_widget(page_content)

    def go_to_camera_page(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "camera_page"

    def go_to_display_page(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "display_page"

    def go_to_manual_card_page(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "manual_card_add_page"
