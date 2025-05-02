from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout


class Example(MDApp):
    def build(self):
        return (
            MDScreen(
                MDBoxLayout(
                    FitImage(
                        source="assets\images\logo.png",
                        size_hint_y=0.35,
                        pos_hint={"top": 1},
                        radius=(dp(36), dp(36), 0, 0),
                    ),
                    radius=dp(36),
                    md_bg_color=self.theme_cls.onSurfaceVariantColor,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    size_hint=(0.4, 0.8),
                ),
            )
        )


Example().run()