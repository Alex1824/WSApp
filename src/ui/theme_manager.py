from kivymd.app import MDApp

class ThemeManager:
    def __init__(self):
        self.dark_mode = False
        self.app = MDApp.get_running_app()
        
    #def toggle_theme(self):
        # self.dark_mode = not self.dark_mode
        # self.app.theme_cls.theme_style = "Dark" if self.dark_mode else "Light"
        # self.app.theme_cls.backgroundColor = "Dark" if self.dark_mode else "Light"
        # print(self.app.theme_cls.backgroundColor)
    #     return self.get_theme_colors()
        
    # def get_theme_colors(self):
    #     if self.dark_mode:
    #         return self.app.theme_cls.theme_style
    #     else:
    #         return self.app.theme_cls.theme_style