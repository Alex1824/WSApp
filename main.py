from kivymd.app import MDApp
from src.views.main_view import MainView
import src.backout.config_db as db

class WhatsAppLinkApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def build(self):
        
        # Crear y retornar la vista principal dentro de un MDScreen
        main_view = MainView(db.managers)
        
        # Configurar tamaño de ventana si no es móvil
        if not self.is_mobile():
            from kivy.core.window import Window
            Window.size = (400, 800)  # Tamaño ideal para esta aplicación
        
        return main_view
    
    def is_mobile(self):
        """Detecta si la aplicación se ejecuta en dispositivo móvil"""
        from kivy.utils import platform
        return platform in ('android', 'ios')

if __name__ == '__main__':
    WhatsAppLinkApp().run()