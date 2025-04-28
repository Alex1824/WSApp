from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import (
    MDButton,
    MDButtonIcon,
    MDButtonText,
    MDIconButton,
    MDFabButton,
    MDExtendedFabButton,
    MDExtendedFabButtonIcon,
    MDExtendedFabButtonText
)

class UIManager:
    @staticmethod
    def create_button(
        text=None,
        callback=None,
        style="elevated",
        icon=None,
        bg_color=None,
        size_hint=(1, None),
        height=dp(50),
        **kwargs
    ):
        """
        Crea un botón MD3 estándar con múltiples variantes
        Args:
            style: "elevated", "filled", "tonal", "outlined", "text"
            icon: Nombre del icono MDI (opcional)
        """
        content = []
        
        if icon:
            content.append(MDButtonIcon(icon=icon))
        if text:
            content.append(MDButtonText(text=text))
        
        return MDButton(
            *content,
            style=style,
            on_release=callback,
            size_hint=size_hint,
            height=height,
            md_bg_color=bg_color,
            **kwargs
        )

    @staticmethod
    def create_icon_button(
        icon,
        callback=None,
        theme_icon_color="Primary",
        size_hint=(None, None),
        size=(dp(48), dp(48)),
        **kwargs
    ):
        """Crea un botón de ícono circular"""
        return MDIconButton(
            icon=icon,
            on_release=callback,
            theme_icon_color=theme_icon_color,
            size_hint=size_hint,
            size=size,
            **kwargs
        )

    @staticmethod
    def create_fab_button(
        icon,
        callback=None,
        type="standard",
        text=None,
        bg_color=None,
        **kwargs
    ):
        """
        Crea un botón de acción flotante (FAB)
        Args:
            type: "standard", "small", "large", "extended"
        """
        if type == "extended":
            content = []
            if icon:
                content.append(MDExtendedFabButtonIcon(icon=icon))
            if text:
                content.append(MDExtendedFabButtonText(text=text))
            
            return MDExtendedFabButton(
                *content,
                on_release=callback,
                md_bg_color=bg_color,
                **kwargs
            )
        else:
            return MDFabButton(
                icon=icon,
                on_release=callback,
                md_bg_color=bg_color,
                size=type,  # "small", "standard", "large"
                **kwargs
            )

    @staticmethod
    def create_text_input(hint_text="", mode="filled", size_hint=(1, None), height=dp(50), **kwargs):
        """Crea un campo de texto MD3"""
        return MDTextField(
            hint_text=hint_text,
            mode=mode,  # "fill", "outlined", "rectangle"
            size_hint=size_hint,
            height=height,
            **kwargs
        )

    @staticmethod
    def create_hyperlink_button(text="", on_press=None, **kwargs):
        """Crea un botón de texto estilo hipervínculo"""
        return MDButton(
            MDButtonText(
                text=text,
                theme_text_color="Custom",
                text_color=get_color_from_hex('#0645AD'),
            ),
            style="text",
            size_hint=(1, None),
            height=dp(50),
            on_release=on_press,
            #underline=True,
            **kwargs
        )

    @staticmethod
    def create_dropdown(caller, options, callback, position="bottom", width_mult=4):
        """
        Crea un menú dropdown moderno (reemplazo de spinner)
        
        Ejemplo de uso:
        def show_dropdown(instance):
            options = [
                {"text": "Opción 1", "on_release": lambda: callback("Opción 1")},
                {"text": "Opción 2", "on_release": lambda: callback("Opción 2")},
            ]
            dropdown = UIManager.create_dropdown(
                caller=instance,
                options=options,
                callback=self.handle_selection
            )
            dropdown.open()
        """
        menu_items = [
            {
                "text": option["text"],
                #"viewclass": "OneLineListItem",
                "on_release": option["on_release"],
            } for option in options
        ]
        
        return MDDropdownMenu(
            caller=caller,
            items=menu_items,
            #position=position,
            #width_mult=width_mult,
        )

    @staticmethod
    def create_country_dropdown(caller, countries, on_select):
        """Versión específica para selección de países"""
        options = [
            {
                "text": country,
                "on_release": lambda x=country: menu_callback(on_select(x)),
            } for country in countries
        ]
        
        def menu_callback(self, text_item):
            self.root.ids.drop_text.text = text_item
        
        return UIManager.create_dropdown(
            caller=caller,
            options=options,
            callback=on_select
        )