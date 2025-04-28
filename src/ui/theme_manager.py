from kivymd.app import MDApp

class ThemeManager:
    def __init__(self):
        self.dark_mode = False
        self.app = MDApp.get_running_app()
        
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.app.theme_cls.theme_style = "Dark" if self.dark_mode else "Light"
        return self.get_theme_colors()
        
    def get_theme_colors(self):
        if self.dark_mode:
            return {
                'background': [0.1, 0.1, 0.1, 1],
                'text': [1, 1, 1, 1],
                'primary': self.app.theme_cls.primary_color
            }
        else:
            return {
                'background': [1, 1, 1, 1],
                'text': [0, 0, 0, 1],
                'primary': self.app.theme_cls.primary_color
            }