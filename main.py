from kivymd.app import MDApp
from kivy.resources import resource_add_path
from os.path import join, dirname
#from src.ui.theme_manager import ThemeManager
from src.managers.ad_manager import AdManager
from src.managers.contact_manager import ContactManager
from src.managers.language_manager import LanguageManager
from src.core.link_manager import LinkManager
from src.managers.history_manager import HistoryManager
from src.views.main_view import MainView

class WhatsAppLinkApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Configuración inicial del tema
        
        # self.theme_cls.material_style = "M3"  # Material Design 3
    
    def build(self):
        # Configuración de rutas de recursos
        resource_add_path(join(dirname(__file__), 'assets'))
        resource_add_path(join(dirname(__file__), 'assets/images'))
        resource_add_path(join(dirname(__file__), 'assets/icons'))
        
        # Inicialización de managers
        managers = {
            'theme':'', #ThemeManager(),
            'ad': AdManager(app_id="ca-app-pub-7788178322918855/5307920549"),
            'contact': ContactManager(),
            'language': LanguageManager(),
            'link': LinkManager(),
            'history': HistoryManager(self.user_data_dir)
        }
        
        # Mostrar anuncios si no es premium
        managers['ad'].show_banner()
        
        # Crear y retornar la vista principal dentro de un MDScreen
        main_view = MainView(managers)
        
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