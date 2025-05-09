from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.metrics import sp
from src.core.phone_utils import get_country_flag

from kivymd.app import MDApp

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDIcon:
        icon: app.flags
        theme_font_name: "Custom"
        font_name: "MaterialSymbols"
        pos_hint: {"center_x": .5, "center_y": .58}

    MDButton:
        pos_hint: {"center_x": .5, "center_y": .47}

        MDButtonIcon:
            icon: app.flags
            theme_font_name: "Custom"
            font_name: "MaterialSymbols"

        MDButtonText:
            text: "Elevated"
'''


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        LabelBase.register(
            name="MaterialSymbols",
            fn_regular="assets/fonts/BabelStoneFlags.ttf",
        )
        
        self.flags=get_country_flag("br")

        self.theme_cls.font_styles["MaterialSymbols"] = {
            "large": {
                "line-height": 1.64,
                "font-name": "MaterialSymbols",
                "font-size": sp(57),
            },
            "medium": {
                "line-height": 1.52,
                "font-name": "MaterialSymbols",
                "font-size": sp(45),
            },
            "small": {
                "line-height": 1.44,
                "font-name": "MaterialSymbols",
                "font-size": sp(36),
            },
        }

        return Builder.load_string(KV)


Example().run()