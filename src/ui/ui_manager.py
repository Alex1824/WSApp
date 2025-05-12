from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.textfield import MDTextField,MDTextFieldHintText,MDTextFieldHelperText,MDTextFieldTrailingIcon
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
from kivymd.uix.boxlayout import MDBoxLayout

class UIManager:
    @staticmethod
    def create_button(
        text=None,
        callback=None,
        style="elevated",
        icon=None,
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
            **kwargs
        )

    @staticmethod
    def create_icon_button(
        icon,
        callback=None,
        **kwargs
    ):
        """Crea un botón de ícono circular"""
        return MDIconButton(
            icon=icon,
            on_release=callback,
            **kwargs
        )

    @staticmethod
    def create_fab_button(
        icon,
        callback=None,
        type="standard",
        text=None,
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
                **kwargs
            )
        else:
            return MDFabButton(
                icon=icon,
                on_release=callback,
                size=type,  # "small", "standard", "large"
                **kwargs
            )

    @staticmethod
    def create_text_input(hint_text=None, mode="filled",icon="", size_hint_x=(1, None), height=dp(50), **kwargs):
        """Crea un campo de texto MD3"""
        content=[]
        content.append(
            MDTextFieldHintText(
            text= hint_text
            )
            )
        # content.append(
        #     MDTextFieldHelperText(
        #     text= hint_text
        #     )
        #     )
        content.append(
            MDTextFieldTrailingIcon(
                icon=icon,
            )
        )
        
        return MDTextField(
            *content,
            mode=mode,  # "fill", "outlined", "rectangle"
            size_hint_x=size_hint_x,
            #height=height,
            **kwargs,
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
            size_hint=(None, None),
            pos_hint={'center_x':.5},
            height=dp(50),
            on_release=on_press,
            **kwargs
        )

    @staticmethod
    def create_dropdown(caller, options):
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
                "on_release": option["on_release"],
            } for option in options
        ]
        
        return MDDropdownMenu(
            caller=caller,
            items=menu_items,
        )

    @staticmethod
    def create_country_dropdown(caller, countries, on_select):
        """Versión específica para selección de países"""
        options = [
            {
                "text": country,
                "on_release": lambda x=country: on_select(x),
            } for country in countries
        ]
        
        return UIManager.create_dropdown(
            caller=caller,
            options=options,
            callback=on_select
        )
        
    @staticmethod
    def create_box_layout(**kwags):
        return MDBoxLayout(**kwags)