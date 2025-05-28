from kivymd.uix.screen import MDScreen
from kivymd.uix.fitimage import FitImage
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText ,MDFabButton
from kivymd.uix.textfield.textfield import MDTextFieldHintText
from kivy.metrics import dp
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from src.ui.ui_manager import UIManager
from logging import Logger
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarText
from kivy.core.clipboard import Clipboard
from kivymd.uix.label import MDLabel,MDIcon
from kivymd.uix.card import MDCard
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
    MDListItemSupportingText)
from kivymd.uix.divider import MDDivider
from kivy.uix.widget import Widget
import logging
from src.core.phone_utils import (
    get_country_code_by_location,
    get_country_flag,
    get_country_code_by_alpha2)
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.clock import mainthread
from kivy.utils import platform
if platform == 'android':
    from android.permissions import request_permissions, Permission, check_permission

class MainView(MDScreen):
    def __init__(self, managers, **kwargs):
        super().__init__(**kwargs)
        self.name = "main_screen"  # Identificador para navegación
        self.ui_manager = UIManager()
        self.language_manager = managers['language']
        self.theme_manager = managers['theme']
        self.link_manager = managers['link']
        self.contact_manager = managers['contact']
        self.history_manager = managers['history']
        self.ad_manager = managers['ad']
        self.is_premium = False
        self.md_bg_color=self.theme_cls.surfaceColor
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.backgroundColor
        
        LabelBase.register(
            name="BabelStoneFlags",
            fn_regular="assets/fonts/BabelStoneFlags.ttf",
        )
        self.theme_cls.font_styles["BabelStoneFlags"] = {
            "standrd": {
                "font-name": "assets/fonts/BabelStoneFlags.ttf",
            }}
        
        self.setup_ui()
        
        self.generated_link_text = ""

    def use_clipboard_number(self, *args):
        """Usa el número de teléfono del portapapeles y cierra el diálogo."""
        if self.link_manager and self.link_manager.last_clipboard:
            self.phone_input.text = self.link_manager.last_clipboard
            Logger.info("MainView: Used phone number from clipboard: %s", self.link_manager.last_clipboard)
        else:
            Logger.warning("MainView: use_clipboard_number called but no clipboard data in link_manager.")
        self.dismiss_dialog() # Asegúrate que self.dismiss_dialog() maneja self.dialog = None
        
    @mainthread  # Decora on_valid_clipboard para ejecutarlo en el hilo principal
    def on_valid_clipboard(self, instance, is_valid):
        """
        Displays a dialog if a valid phone number is found in the clipboard.
        This function is called when the is_valid_clipboard property of LinkManager changes.

        Args:
            instance: The LinkManager instance.
            is_valid: A boolean indicating whether the clipboard contains a valid phone number.
        """
        if is_valid:
            Logger.debug("MainView: Valid phone number detected in clipboard.")  # Registro
            if not self.dialog:  # Verifica si el diálogo ya existe
                self.dialog = MDDialog(
                    title=self.language_manager.get_text('use_clipboard_title'),
                    text=self.language_manager.get_text('use_clipboard_text'),
                    buttons=[
                        MDFabButton(
                            text=self.language_manager.get_text('cancel'),
                            on_release=self.dismiss_dialog,
                        ),
                        MDButton(  # Usar MDButton con style="elevated"
                            text=self.language_manager.get_text('use'),
                            on_release=self.use_clipboard_number,
                            style="elevated",  # Establecer el estilo a "elevated"
                        ),
                    ],
                )
            self.dialog.open()
        else:
            Logger.debug("MainView: Invalid phone number in clipboard.")  # Registro
            if self.dialog:  # Añadido para cerrar el diálogo si ya no es válido
                self.dialog.dismiss()
                self.dialog = None


    def dismiss_dialog(self, *args):
        """Closes the dialog and resets it."""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None  # Importante: Elimina la referencia al diálogo        
        
        
    def setup_ui(self):
        
        screen_width = Window.size[0]
        screen_height = Window.size[1]
        max_width = dp(400)
        max_height = dp(800)
        
        # Calculate ScrollView size
        content_width = min(screen_width, max_width)
        content_height = min(screen_height, max_height+10)
        
        
            # Scrollable content
        self.main_box = MDScrollView(
            size_hint=(None, None),
            size=(content_width,content_height),
            do_scroll_x=False,
            do_scroll_y=False,
            radius=[dp(20)],
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Centra
        )
        
        # Card for shadow effect
        self.card = MDCard(
                style="elevated",
                size_hint=(None, None),
                size=(content_width, content_height),
                radius=[dp(20)],
                pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Centra
                theme_shadow_color="Custom",
                shadow_color="green",
                theme_bg_color="Custom",
                md_bg_color="white",
                md_bg_color_disabled="grey",
                theme_shadow_offset="Custom",
                shadow_offset=(1, -2),
                theme_shadow_softness="Custom",
                shadow_softness=1,
                theme_elevation_level="Custom",
                elevation_level=3,
        )

        # Layout principal
        self.layout = self.ui_manager.create_box_layout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,  # Permite que el layout se expanda verticalmente
            adaptive_height=True, # El alto del layout se ajusta a su contenido
            width=content_width, # El ancho es el del scrollview
            radius=dp(20),
            
            
    )
        
        self.logo_continer = self.ui_manager.create_box_layout(
            radius=dp(40),
            pos_hint={"center_x": .5, "center_y": .5},
            size_hint=(None, None),
            adaptive_height=True,
            adaptive_width=True,
            )
        
        # Logo
        logo = FitImage(
            source="assets/images/WSion.png",
            size_hint=(None,None),
            size=(dp(150),dp(150)),
            fit_mode='contain',
            radius=dp(40),
        )
        
        self.lang_btn_box=self.ui_manager.create_box_layout(
            orientation="vertical",
            pos_hint={'left':1},
            adaptive_height=True,
            adaptive_width=True,
            size_hint_y=None,
            size_hint_x=.6
        )     
    
        # Language selector (ahora como dropdown)
    
        self.language_button = self.ui_manager.create_button(
            text=self.language_manager.current_language,
            icon="translate",
            style="outlined",
            callback=self.show_language_menu,
            size_hint_max_x=.6,
            size_hint=(None,None),
        )
        
        self.logo_continer.add_widget(logo)
        self.layout.add_widget(self.logo_continer)
        self.lang_btn_box.add_widget(self.language_button)
        self.layout.add_widget(self.lang_btn_box)
        
        # Phone input section
        self.setup_phone_input()
        
        # Action buttons
        self.setup_action_buttons()
        
        self.main_box.add_widget(self.layout)
        self.card.add_widget(self.main_box)
        self.add_widget(self.card)
        
        
        
    def setup_phone_input(self):
                
        # Country selection
        country_box = self.ui_manager.create_box_layout(
            orientation="horizontal",
            pos_hint={'left':1},
            adaptive_height=True,
            size_hint_y=None,
            size_hint_x=.5,
            spacing=dp(10),
            )
        
        self.country_filter = self.ui_manager.create_text_input(
            hint_text=self.language_manager.get_text('search_country'),
            pos_hint={'left':1},
            size_hint_x=0.5,
        )
        # Set name for the hint text child
        if self.country_filter.children and isinstance(self.country_filter.children[0], MDTextFieldHintText):
            self.country_filter.children[0].name = 'search_country'
        
        flag_box=self.ui_manager.create_box_layout(
            orientation="horizontal",
            adaptive_width=True,
            size_hint_x=dp(0.13),
            pos_hint={'right':1},
        )
        
        self.flag_label = MDIcon(
            size_hint=(1, None),
            pos_hint= {"center_x":.5,"center_y": 0.5},
        )
        
        flag_box.add_widget(self.flag_label)
        
        self.is_premium=True
        country_box.add_widget(self.country_filter)
        # Auto-detect country if premium
        if self.is_premium:
            detected_country = get_country_code_by_location()
            if detected_country:
                self.country_filter.text = get_country_code_by_alpha2(detected_country)
                self.flag_label.icon= get_country_flag(detected_country)
                country_box.add_widget(flag_box)
        
        self.country_filter.bind(
            text=lambda instance, value: self.update_flag(value),
        )
        
        self.layout.add_widget(country_box)
        
        # Phone number input
        self.phone_input = self.ui_manager.create_text_input(
            hint_text=self.language_manager.get_text('enter_phone'),
            icon="phone",
            size_hint_x=0.9,
        )
        if self.phone_input.children and isinstance(self.phone_input.children[0], MDTextFieldHintText):
            self.phone_input.children[0].name = 'enter_phone'
        self.layout.add_widget(self.phone_input)
        
        # Custom message input
        self.message_input = self.ui_manager.create_text_input(
            hint_text=self.language_manager.get_text('custom_message'),
            multiline=True,
            icon="email",
            max_height= "200dp",
            size_hint_x=0.9,
        )
        if self.message_input.children and isinstance(self.message_input.children[0], MDTextFieldHintText):
            self.message_input.children[0].name = 'custom_message'
        self.layout.add_widget(self.message_input)
    
    def update_flag(self, country_code):
        self.flag_label.icon = get_country_flag(country_code)
            
    def setup_action_buttons(self):
        
        button_box = self.ui_manager.create_box_layout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(10),
            pos_hint={'center_x':.5,'center_y':.5},
        )
        
        btn_valid=self.ui_manager.create_button(
            self.language_manager.get_text('validate_link'),
            self.on_validate, 
            "filled", 
            "check",
            pos_hint={'center_x':.5},
            )
        # Set name for the button text child
        if btn_valid.children and isinstance(btn_valid.children[0], MDButtonText):
            btn_valid.children[0].name = 'validate_link'
        
        button_column = self.ui_manager.create_box_layout(
            orientation="horizontal",
            spacing=dp(5),
            size_hint=(1,None),
            height=dp(48), # set the height of the boxlayout
            center=(.5,5)
        )
        
        # Define tooltip keys corresponding to icons
        tooltip_keys = {
            "content-copy": "copy_link_tooltip",
            "share-variant": "share_link_tooltip",
            "account-box": "select_contact_tooltip",
            "history": "view_history_tooltip",
            "crown": "go_premium_tooltip",
            "theme-light-dark": "toggle_theme_tooltip"
        }

        buttons_data = [
            # text_key is None for icon buttons, callback, style, icon_name
            (None, self.on_copy, "elevated", "content-copy"),
            (None, self.on_share, "elevated", "share-variant"),
            (None, self.on_select_contact, "tonal", "account-box"),
            (None, self.on_history, "tonal", "history"),
            (None, self.on_premium, "filled", "crown"),
            (None, self.on_theme_toggle, "filled", "theme-light-dark")
        ]
        
        for text_key, callback, style, icon_name in buttons_data:
            # Assuming create_button creates an MDIconButton or similar when text is None
            # and that it supports setting tooltip_text.
            # The 'name' attribute will be used by a hypothetical update method for tooltips.
            btn = self.ui_manager.create_button(
                text=self.language_manager.get_text(text_key) if text_key else "", # Ensure text is not None
                callback=callback,
                style=style,
                icon=icon_name, # Use icon_name consistently
                size_hint_x=None,  # Don't restrict button width, the boxlayout will manage it
                tooltip_text=self.language_manager.get_text(tooltip_keys.get(icon_name)) # Set initial tooltip
            )
            # Set the name attribute for future tooltip updates
            btn.name = tooltip_keys.get(icon_name) 
            button_column.add_widget(btn)
        
        # Link display
        self.link_button = self.ui_manager.create_hyperlink_button(
            text=self.language_manager.get_text('generated_link'),
            on_press=self.on_link_press,
            md_bg_color = self.theme_cls.surfaceColor,
        )
        if self.link_button.children and isinstance(self.link_button.children[0], MDButtonText):
            self.link_button.children[0].name = 'generated_link'
            
        self.layout.add_widget(button_box)
        button_box.add_widget(btn_valid)
        button_box.add_widget(button_column)
        button_box.add_widget(self.link_button)
    
    def show_language_menu(self, instance):
        languages = [
            {
                "text": lang,
                "on_release": lambda x=lang: self.on_language_change(x)
            } for lang in self.language_manager.get_available_languages()
        ]
        self.language_dropdown = self.ui_manager.create_dropdown(
            caller=instance,
            options=languages 
        )
        self.language_dropdown.open()
    
        
    def on_language_change(self, language):
        self.language_dropdown.dismiss()
        self.language_manager.change_language(language)
        self.language_button.children[0].text = language  # Actualiza texto del botón
        self.update_texts()
    
    def on_validate(self, instance):
        """Validate and generate WhatsApp link"""
        
        # Clear previous error if any
        self.phone_input.error = False
        self.phone_input.helper_text = "" 

        # Initial validation for empty phone number
        if not self.phone_input.text.strip(): # Verifica si está vacío o solo espacios
            self.phone_input.error = True
            # Usa helper_text para el mensaje de error, no el hint_text.
            self.phone_input.helper_text = self.language_manager.get_text('error_phone_required') 
            return

        # Proceed with link generation if initial validation passes
        success, result = self.link_manager.generate_link(
            self.phone_input.text,
            self.country_filter.text,
            self.message_input.text
        )

        if success:
            # Check if result is a tuple (link, message) for country detection
            if isinstance(result, tuple):
                link, message = result
                self.generated_link_text = link
                self.show_country_detected_dialog(message, link)
                
            else:
                # Successfully generated link directly
                self.generated_link_text = result
                link_button_text =[
                    child 
                    for child in self.link_button.walk()
                    if isinstance(child, MDButtonText)                   
                ]
                link_button_text[0].text = f"{result}" # Update button text with underline
                # Use theme color for success (usually primary or accent)
                self.link_button.theme_text_color = "Primary"
                self.history_manager.add_link(result)
                # AnimationManager.highlight_input(self.phone_input, success=True) # Adapt/replace
        else:
            # Failed validation or generation
            error_message = result or self.language_manager.get_text('error_invalid_input')
            self.generated_link_text = "" # Clear generated link
            self.link_button.text = f"{self.language_manager.get_text('generated_link')}" # Reset text
            # Use error color for link button (or keep it neutral)
            # KivyMD doesn't have a direct error color for buttons, maybe change text?
            self.link_button.theme_text_color = "Error" # Set text color to theme's error color
            # Show error on the relevant input field
            self.phone_input.error = True
            self.phone_input.helper_text = error_message
            # AnimationManager.highlight_input(self.phone_input, success=False) # Adapt/replace


    def show_country_detected_dialog(self, message, link):
        """elevated when country code is detected/guessed"""
        dialog = UIManager.create_confirmation_dialog(
            title=self.language_manager.get_text('country_detected'),
            text_content=message,
            on_yes_callback=lambda: self._accept_detected_country(link),
            on_no_callback=lambda: None, # Do nothing on "No"
            language_manager=self.language_manager
        )
        dialog.open()

    def _accept_detected_country(self, link):
        """Action when user accepts the detected country link"""
        self.generated_link_text = link
        self.link_button.text = f"{link}"
        self.link_button.theme_text_color = "Primary"
        self.history_manager.add_link(link)
        # AnimationManager.highlight_input(self.phone_input, success=True) # Adapt/replace

    def on_copy(self, instance):
        """Copy generated link to clipboard"""
        if self.generated_link_text:
            Clipboard.copy(self.generated_link_text)
            # Show feedback using MDSnackbar
            MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('link_copied'))).open()
            # AnimationManager.button_press(instance) # Adapt/replace
        else:
            MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('error_no_link_to_copy'))).open()

    def on_select_contact(self, instance):
        """Handles the contact selection button press, initiating permission check if needed."""
        if platform == 'android':
            if not check_permission(Permission.READ_CONTACTS):
                Logger.info("MainView: Requesting READ_CONTACTS permission.")
                request_permissions([Permission.READ_CONTACTS], self._on_contact_permission_result)
                return 
            else:
                Logger.info("MainView: READ_CONTACTS permission already granted.")
                self._show_contact_dialog() 
        else:
            # For non-Android platforms, proceed directly
            Logger.info("MainView: %s", "Not on Android, proceeding to show contact dialog.")
            self._show_contact_dialog()

    def _on_contact_permission_result(self, permissions, grant_results):
        """Callback for the Android permission request."""
        if permissions and Permission.READ_CONTACTS in permissions: # Check if READ_CONTACTS was in the request
            permission_index = permissions.index(Permission.READ_CONTACTS)
            if grant_results and grant_results[permission_index]:
                Logger.info("MainView: READ_CONTACTS permission granted by user.")
                self._show_contact_dialog()
            else:
                Logger.warning("MainView: READ_CONTACTS permission denied by user.")
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('error_contact_permission_denied'))).open()
        else:
            Logger.warning("MainView: READ_CONTACTS permission result callback received for an unexpected permission request.")


    def _show_contact_dialog(self):
        """Shows the contact selection dialog after permissions are confirmed."""
        try:
            contacts = self.contact_manager.get_contacts()
            if not contacts:
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('error_no_contacts'))).open()
                return

            items = []
            # This dialog instance needs to be accessible to the callback.
            # We can pass it or make it an instance variable if absolutely necessary,
            # but for this structure, defining it before the callback that needs it is key.
            self.contact_dialog_instance = None # Ensure it's reset or managed if dialogs can overlap

            def contact_selected_callback(contact_number, contact_name):
                self.phone_input.text = contact_number
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('contact_selected') + f": {contact_name}")).open()
                if self.contact_dialog_instance: 
                    self.contact_dialog_instance.dismiss()
                # AnimationManager.highlight_input(self.phone_input) # Adapt/replace

            for contact in contacts:
                items.append(
                    MDListItem(
                        text=f"{contact.get('name', 'Unknown')} ({contact.get('number', 'No number')})",
                        on_release=lambda x, num=contact.get('number'), name=contact.get('name'): contact_selected_callback(num, name) if num else None
                    )
                )
            
            self.contact_dialog_instance = MDDialog(
                title=self.language_manager.get_text('select_contact_title'),
                type="simple",
                items=items,
                size_hint=(0.9, 0.8)
            )
            self.contact_dialog_instance.open()

        except Exception as e:
            Logger.error(f"MainViewMD: Error getting or displaying contacts in _show_contact_dialog: {e}")
            MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('error_contact_access'))).open()

    def on_share(self, instance):
        """Share the generated link"""
        if not self.generated_link_text:
            MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('error_no_link_to_share'))).open()
            return

        link_to_share = self.generated_link_text
        # Use plyer for cross-platform sharing if possible
        try:
            from plyer import share
            share.share(text=link_to_share, title='Share WhatsApp Link')
            # AnimationManager.button_press(instance) # Adapt/replace
        except ImportError:
            Logger.warning("Plyer not found. Falling back to platform-specific sharing.")
            # Fallback to original platform-specific code
            from kivy.utils import platform
            if platform == 'android':
                try:
                    from jnius import autoclass
                    Intent = autoclass('android.content.Intent')
                    String = autoclass('java.lang.String')
                    intent = Intent()
                    intent.setAction(Intent.ACTION_SEND)
                    intent.setType('text/plain')
                    intent.putExtra(Intent.EXTRA_TEXT, String(link_to_share))
                    chooser = Intent.createChooser(intent, String('Share WhatsApp Link'))
                    # Get activity reference safely from MDApp
                    current_activity = self.AndroidActivity
                    if current_activity:
                        current_activity.startActivity(chooser)
                    else:
                        Logger.error("Could not get Android activity reference.")
                        Clipboard.copy(link_to_share) # Fallback to copy
                        MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('link_copied_share_failed'))).open()

                except Exception as e:
                    Logger.error(f'Error sharing link on Android: {str(e)}')
                    Clipboard.copy(link_to_share) # Fallback to copy
                    MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('link_copied_share_failed'))).open()
            else: # Other platforms (iOS, Desktop) - Copy to clipboard
                Clipboard.copy(link_to_share)
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('link_copied_share_unavailable'))).open()
        except Exception as e:
            Logger.error(f'Error using Plyer share: {str(e)}')
            Clipboard.copy(link_to_share) # Fallback to copy
            MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('link_copied_share_failed'))).open()

    def on_premium(self, instance):
        """Show premium purchase dialog or indicate premium status"""
        if not self.is_premium:
            # --- Show Premium Purchase Dialog ---
            dialog = None # Define dialog variable first

            # Content for the dialog (Using MDLabel for features)

            dialog =MDDialog(
                # ----------------------------Icon-----------------------------
                    MDDialogIcon(
                        icon="crown",
                    ),
                    # -----------------------Headline text-------------------------
                    MDDialogHeadlineText(
                        text=self.language_manager.get_text('premium_title'),
                    ),
                    # -----------------------Supporting text-----------------------
                    MDDialogSupportingText(
                        text=self.language_manager.get_text('premium_features'),
                    ),
                    # -----------------------Custom content------------------------
                    MDDialogContentContainer(
                    
                        MDDivider(),
                        MDListItem(
                            MDListItemLeadingIcon(
                                icon="check",
                            ),
                            MDListItemSupportingText(
                                text=self.language_manager.get_text('auto_country'), 
                                adaptive_height=True, 
                                theme_text_color="Secondary"
                            ),
                            theme_bg_color="Custom",
                            md_bg_color=self.theme_cls.transparentColor,
                        ),
                        MDListItem(
                            MDListItemLeadingIcon(
                                icon="check",
                            ),
                            MDListItemSupportingText(
                                text=self.language_manager.get_text('ip_detection'), 
                                adaptive_height=True, 
                                theme_text_color="Secondary"
                            ),
                            theme_bg_color="Custom",
                            md_bg_color=self.theme_cls.transparentColor,
                        ),
                        MDDivider(),
                        orientation="vertical",
                    ),
                    # ---------------------Button container------------------------
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(
                            MDButtonText(
                                text=self.language_manager.get_text('cancel')
                                ),
                            style="elevated",
                            on_press=lambda *args: dialog.dismiss(),
                        ),
                        MDButton(
                            MDButtonText(
                                text=self.language_manager.get_text('buy_premium')
                                                                    ),
                            style="elevated",
                            on_release=lambda *args: (self._activate_premium, dialog.dismiss()),
                        ),
                        spacing="15dp",
                        ),
                    )
            dialog.open()
        else:
            # Already premium - show a MDSnackbar message
            MDSnackbar(
                MDSnackbarText(
                    text=self.language_manager.get_text('premium_active'),
                    ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                ).open()


    def _activate_premium(self):
        """Action when user clicks 'Buy' in premium dialog"""
        # --- This is where the actual purchase logic would go ---
        # For now, we just simulate success
        Logger.info("Simulating Premium Activation")
        self.app.is_premium = True # Update app's premium status
        # self.is_premium is updated automatically via binding (_update_local_premium)

        # Update UI elements related to premium status
        self.update_premium_ui_elements()

        # Hide ads via manager
        try:
            self.ad_manager.hide_banner()
        except Exception as e:
            Logger.error(f"Failed to hide banner ad: {e}")

        MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('premium_activated_success'))).open()


    def update_premium_ui_elements(self):
        """Update UI elements based on premium status"""
        # Example: Change premium button text/icon and disable if needed
        if self.is_premium:
            if self.premium_button:
                self.premium_button.text = self.language_manager.get_text('premium_active')
                # Optionally change icon or disable
                # self.premium_button.icon = "check-decagram"
                self.premium_button.disabled = True
            # Enable premium features in UI if they were disabled
            # e.g., make country detection logic run if it was previously skipped
            if self.country_filter and not self.country_filter.text:
                # Trigger auto-detection again if it wasn't done before
                try:
                    from ..core.phone_utils import get_country_code_by_location, get_country_flag
                    detected_country = get_country_code_by_location()
                    if detected_country:
                        self.country_filter.text = detected_country
                        self.flag_label.text = get_country_flag(detected_country)
                except Exception as e:
                    Logger.error(f"Error detecting country after premium activation: {e}")

        else:
            # Revert UI elements if premium status is lost
            if self.premium_button:
                self.premium_button.text = self.language_manager.get_text('go_premium')
                # self.premium_button.icon = "crown"
                # self.premium_button.disabled = False
            # Disable premium features here if necessary


    def on_theme_toggle(self, instance):
        """Toggle between light and dark themes"""
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        self.card.md_bg_color=self.theme_cls.backgroundColor if self.theme_cls.theme_style == "Dark" else "white"

    def on_history(self, instance):
        """Show history dialog"""
        try:
            history_list = self.history_manager.get_history()
            
            if not history_list:
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('history_empty'))).open()
                return

            def _history_item_selected(link):
                self.phone_input.text = ''  # Clear inputs
                self.message_input.text = ''
                self.country_filter.text = ''
                self.generated_link_text = link  # Set selected link as current
                self.link_button.text = link
                self.link_button.theme_text_color = "Primary"
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('history_link_loaded'))).open()
                dialog.dismiss()

        # Crear la lista de items del historial
            items = []
            for link in reversed(history_list):
                items.append(
                    MDListItem(
                        MDListItemLeadingIcon(
                            icon="link"
                        ),
                        MDListItemSupportingText(
                            text=str(link)
                        ),
                        on_release=lambda x, l=link: _history_item_selected(l),
                        radius=dp(10),
                    )
                )

            # Crear el BoxLayout para los items
            items_layout = self.ui_manager.create_box_layout(
                orientation="vertical",
                spacing="8dp",
                #padding=("12dp", "8dp", "12dp", "8dp"),
            )
            for item in items:
                items_layout.add_widget(item)

            # Crear el ScrollView
            scroll_view = MDScrollView(
                size_hint=(1, None),
                height="400dp"  # Altura máxima del ScrollView
            )
            scroll_view.add_widget(items_layout)

            # Crear el diálogo
            dialog = MDDialog(
                MDDialogIcon(
                    icon="history"
                ),
                MDDialogHeadlineText(
                    text=self.language_manager.get_text('history_title')
                ),
                MDDialogContentContainer(
                    MDDivider(),
                    scroll_view,
                    MDDivider(),
                    orientation="vertical",
                    #padding=("24dp", "16dp", "24dp", "24dp"),
                    spacing="16dp"
                ),
                size_hint=(.9, None),
                height="500dp"  # Altura total del diálogo
            )
            
            dialog.open()

        except Exception as e:
            Logger.error(f"MainViewMD: Error getting or displaying history: {e}")
            MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('error_history_access'))).open()

    def on_link_press(self, instance):
        """Handle link button press - open in browser"""
        if self.generated_link_text:
            try:
                from webbrowser import open as open_url
                open_url(self.generated_link_text)
            except Exception as e:
                logging.error(f"Failed to open link: {e}")
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('error_opening_link'))).open()


    def _update_button_texts(self):
        """Update texts for MDButtons using widget.name as the language key."""
        Logger.debug("MainView: Starting _update_button_texts")
        for child in self.layout.walk():
            if isinstance(child, MDButton):
                for sub_child in child.children: # MDButtonText is often a child of MDButton
                    if isinstance(sub_child, MDButtonText):
                        if hasattr(sub_child, 'name') and sub_child.name:
                            lang_key = sub_child.name
                            translated_text = self.language_manager.get_text(lang_key)
                            if translated_text != lang_key : # Only update if translation exists and is different
                                if sub_child.text != translated_text:
                                    sub_child.text = translated_text
                                    Logger.debug(f"MainView: Updated MDButtonText '{lang_key}' to '{translated_text}'")
                            # else:
                                # Logger.debug(f"MainView: MDButtonText '{lang_key}' not translated or translation is same as key.")
                        # else:
                            # Logger.debug(f"MainView: MDButtonText widget {sub_child} has no 'name' property or it's empty.")


    def _update_text_input_hints(self):
        """Update hint_texts for MDTextFields using hint_widget.name as the language key."""
        from kivy.clock import Clock
        Logger.debug("MainView: Starting _update_text_input_hints")
        text_fields_to_refresh = []

        for child in self.layout.walk():
            if isinstance(child, MDTextFieldHintText): # This is the actual hint text widget
                if hasattr(child, 'name') and child.name:
                    lang_key = child.name
                    translated_text = self.language_manager.get_text(lang_key)
                    
                    # Ensure parent MDTextField is captured for refresh
                    text_field = child.parent 
                    if text_field and text_field not in text_fields_to_refresh:
                         text_fields_to_refresh.append(text_field)

                    if translated_text != lang_key: # Only update if translation exists
                        if child.text != translated_text:
                            child.text = translated_text # Update the hint text itself
                            Logger.debug(f"MainView: Updated MDTextFieldHintText '{lang_key}' to '{translated_text}'")
                    # else:
                        # Logger.debug(f"MainView: MDTextFieldHintText '{lang_key}' not translated or translation is same as key.")
                # else:
                    # Logger.debug(f"MainView: MDTextFieldHintText widget {child} has no 'name' property or it's empty.")
        
        # Force refresh after updating all hints
        def refresh_text_fields(*args):
            Logger.debug("MainView: Refreshing MDTextFields for hint text update.")
            for field in text_fields_to_refresh:
                # A common way to force refresh is to briefly change a property that affects layout/drawing
                original_helper_text = field.helper_text
                field.helper_text = " " 
                field.helper_text = original_helper_text
                # Or try focus, though helper_text change might be more reliable for hints
                # field.focus = True 
                # field.focus = False
            Logger.debug("MainView: Finished refreshing MDTextFields.")

        if text_fields_to_refresh:
            Logger.debug(f"MainView: Scheduling refresh for {len(text_fields_to_refresh)} text fields.")
            Clock.schedule_once(refresh_text_fields, 0)


    def _update_labels(self):
        """Update texts for MDLabels using label.name as the language key."""
        Logger.debug("MainView: Starting _update_labels")
        for child in self.layout.walk():
            if isinstance(child, MDLabel):
                # Exclude MDIcon which is a subclass of MDLabel but should not have its text (icon name) translated
                if isinstance(child, MDIcon):
                    continue
                if hasattr(child, 'name') and child.name:
                    lang_key = child.name
                    translated_text = self.language_manager.get_text(lang_key)
                    if translated_text != lang_key : # Only update if translation exists and is different
                        if child.text != translated_text:
                            child.text = translated_text
                            Logger.debug(f"MainView: Updated MDLabel '{lang_key}' to '{translated_text}'")
                    # else:
                        # Logger.debug(f"MainView: MDLabel '{lang_key}' not translated or translation is same as key.")
                # else:
                    # Logger.debug(f"MainView: MDLabel widget {child} has no 'name' property or it's empty.")


    def update_texts(self):
        """Update all UI texts based on current language."""
        
        self._update_button_texts()
        self._update_text_input_hints()
        self._update_labels()  # Add this line to update 
        

        # Update specific texts outside the loops (as you were doing)
        self.country_filter.hint_text = self.language_manager.get_text('search_country')
        self.phone_input.hint_text = self.language_manager.get_text('enter_phone')
        self.message_input.hint_text = self.language_manager.get_text('custom_message')
        self.link_button.text = self.language_manager.get_text('generated_link')

