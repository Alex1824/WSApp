from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField 
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
from kivymd.uix.list import MDListItem
from kivymd.uix.label import MDLabel,MDIcon
from kivymd.uix.card import MDCard
from kivymd.uix.list import (MDListItem,MDListItemLeadingIcon,MDListItemSupportingText,MDListItemHeadlineText)
from kivymd.uix.divider import MDDivider
from kivy.uix.widget import Widget
import logging
from kivymd.uix.anchorlayout import MDAnchorLayout
from src.core.phone_utils import (
    get_country_code_by_location,
    get_country_flag,
    get_country_code_by_alpha2)
from kivy.core.text import LabelBase

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
        
        # Bind to clipboard changes
        self.link_manager.bind(is_valid_clipboard=self.on_valid_clipboard)
        
        self.setup_ui()
        
    def setup_ui(self):
        
        # Scrollable content
        self.main_box = MDScrollView(
            pos_hint={'right':1,'left':1},
            do_scroll_x=False,
            )

        # Layout principal
        self.layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15),
            adaptive_height=True,
            size_hint=(1,1),
            )
        
        self.logo_continer = MDBoxLayout(
            #radius=dp(40),
            pos_hint={"center_x": .5, "center_y": .5},
            # md_bg_color=self.theme_cls.onSurfaceVariantColor,
            size_hint=(None, None),
            adaptive_height=True,
            adaptive_width=True,
            )
        
        # Logo
        logo = FitImage(
            source="assets/images/WSion.png",
            size_hint=(None,None),
            size=(dp(150),dp(150)),
            fit_mode='contain'
        )
        
        self.lang_btn_box=MDBoxLayout(
            orientation="vertical",
            # md_bg_color=self.theme_cls.onSurfaceVariantColor,
            pos_hint={'left':1},
            adaptive_height=True,
            adaptive_width=True,
            size_hint_y=None,
            size_hint_x=.8
        )     
    

        # Language selector (ahora como dropdown)
    
        self.language_button = self.ui_manager.create_button(
            text=self.language_manager.current_language,
            icon="translate",
            style="outlined",
            callback=self.show_language_menu,
        )
        
        self.logo_continer.add_widget(logo)
        self.layout.add_widget(self.logo_continer)
        self.lang_btn_box.add_widget(self.language_button)
        self.layout.add_widget(self.lang_btn_box)
        
        # Phone input section
        self.setup_phone_input()
        
        # Action buttons
        self.setup_action_buttons()
        
        # Link display
        self.link_button = self.ui_manager.create_hyperlink_button(
            text=self.language_manager.get_text('generated_link'),
            on_press=self.on_link_press,
            md_bg_color = self.theme_cls.surfaceColor
        )
        self.layout.add_widget(self.link_button)
        
        self.main_box.add_widget(self.layout)
        self.add_widget(self.main_box)
        
    def setup_phone_input(self):
                
        # Country selection
        country_box = MDBoxLayout(
            orientation="horizontal",
            pos_hint={'left':1},
            adaptive_height=True,
            size_hint_y=None,
            size_hint_x=1,
            spacing=dp(10),
            )
        
        self.country_filter = self.ui_manager.create_text_input(
            hint_text=self.language_manager.get_text('search_country'),
            pos_hint={'left':1},
            # width= "200dp",
            size_hint_x=0.5,
        )
        
        flag_box=MDBoxLayout(
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
            size_hint_x=0.8,
        )
        self.layout.add_widget(self.phone_input)
        
        # Custom message input
        self.message_input = self.ui_manager.create_text_input(
            hint_text=self.language_manager.get_text('custom_message'),
            multiline=True,
            icon="email",
            # size_hint_x=(dp(100),None),
            max_height= "200dp",
            size_hint_x=0.8,
        )
        self.layout.add_widget(self.message_input)
    
    def update_flag(self, country_code):
        self.flag_label.icon = get_country_flag(country_code)
            
    def setup_action_buttons(self):
        
        button_valid = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True
        )
        
        btn_valid=self.ui_manager.create_button(
            self.language_manager.get_text('validate_link'),
            self.on_validate, 
            "filled", 
            "check",
            pos_hint={'center_x':.5},
            )
        button_valid.add_widget(btn_valid)
        self.layout.add_widget(button_valid)
        
        button_column = MDBoxLayout(
            orientation="horizontal",
            height=dp(50),
            size_hint=(None,None),
            #pos_hint={'center_x': 0.5},
            spacing=dp(10),
            
        )
        
        buttons = [
            (None,self.on_copy, "elevated", "content-copy"),
            (None,self.on_share, "elevated", "share-variant"),
            (None,self.on_select_contact, "tonal", "account-box"),
            (None,self.on_history, "tonal", "history"),
            (None,self.on_premium, "filled", "crown"),
            (None,self.on_theme_toggle,"filled", "theme-light-dark",)
        ]
        
        for text_key, callback, style, icon in buttons:
            btn = self.ui_manager.create_button(
                text=self.language_manager.get_text(text_key),
                callback=callback,
                style=style,
                icon=icon,
            )
        button_column.add_widget(btn)
        
        button_container = MDAnchorLayout(
            anchor_x="center",
        )

        button_container.add_widget(button_column)
        self.layout.add_widget(button_container)
    
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
    
        
    def on_valid_clipboard(self, instance, value):
        """Handle when valid phone number is detected in clipboard"""
        if value and self.link_manager.last_clipboard:
            dialog = MDDialog(
                title=self.language_manager.get_text('clipboard_title'),
                text=self.language_manager.get_text('phone_detected'),
                buttons=[
                    MDButton(
                        text=self.language_manager.get_text('yes'),
                        on_release=lambda _: self.use_clipboard_number()
                    ),
                    MDButton(
                        text=self.language_manager.get_text('no'),
                        on_release=lambda _: dialog.dismiss()
                    ),
                ],
            )
            dialog.open()
        
    def use_clipboard_number(self):
        self.phone_input.text = self.link_manager.last_clipboard
        if hasattr(self, 'clipboard_dialog'):
            self.clipboard_dialog.dismiss()

    def on_validate(self, instance):
        """Validate and generate WhatsApp link"""

        if not self.phone_input.text and not self.phone_input.text.isdecimal():
            self.phone_input.error = True
            self.phone_input.helper_text = self.language_manager.get_text('error_phone_required')
            # AnimationManager.highlight_input(self.phone_input, success=False) # Adapt/replace
            return

        # Clear previous error if any
        
        self.phone_input.error = False
        self.phone_input.helper_text = self.language_manager.get_text('phone_number_hint')

        success, result = self.link_manager.generate_link(
            self.phone_input.text,
            self.country_filter.text,
            self.message_input.text
        )

        if success:
            # Check if result is a tuple (link, message) for country detection
            if isinstance(result, tuple):
                link, message = result
                self.show_country_detected_dialog(message, link)
            else:
                # Successfully generated link directly
                self.generated_link_text = result
                self.link_button.text = f"{result}" # Update button text with underline
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
        """Show contact selection dialog"""
        # Needs replacement for ContactsPopup using KivyMD components
        # Example using a simple MDDialog with a list (requires contact_manager)
        try:
            contacts = self.contact_manager.get_contacts() # [{'name': 'John', 'number': '123'}, ...]
            if not contacts:
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('error_no_contacts'))).open()
                return

            # Create list items for the dialog
            # Using kivymd.uix.list.OneLineAvatarIconListItem would be better if icons/avatars are available
            items = []
            dialog = None # Define dialog first

            def contact_selected_callback(contact_number, contact_name):
                self.phone_input.text = contact_number
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('contact_selected') + f": {contact_name}")).open()
                if dialog:
                    dialog.dismiss()
                # AnimationManager.highlight_input(self.phone_input) # Adapt/replace

            for contact in contacts:
                items.append(
                    MDListItem(
                        text=f"{contact.get('name', 'Unknown')} ({contact.get('number', 'No number')})",
                        on_release=lambda x, num=contact.get('number'), name=contact.get('name'): contact_selected_callback(num, name) if num else None
                    )
                )

            dialog = MDDialog(
                title=self.language_manager.get_text('select_contact_title'),
                type="simple", # Use "simple" type for list items
                items=items,
                size_hint=(0.9, 0.8) # Adjust size
            )
            dialog.open()

        except Exception as e:
            Logger.error(f"MainViewMD: Error getting or displaying contacts: {e}")
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
                    text=self.language_manager.get_text('premium_already_active'),
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
                # self.premium_button.disabled = True
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
        self.layout.md_bg_color=self.theme_cls.backgroundColor
        # Update button text immediately (or refactor update_texts to handle this)
        #self.update_texts() # Call update_texts to refresh button labels
        #AnimationManager.button_press(instance) # Adapt/replace

    def on_history(self, instance):
        """Show history dialog"""
        # Needs replacement for HistoryPopup using KivyMD components
        try:
            history_list = self.history_manager.get_history() # Assume returns list of strings (links)
            if not history_list:
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('history_empty'))).open()
                return

            items = []
            dialog = None

            def history_item_selected(link):
                self.phone_input.text = '' # Clear inputs
                self.message_input.text = ''
                self.country_filter.text = ''
                self.generated_link_text = link # Set selected link as current
                self.link_button.text = f"{link}"
                self.link_button.theme_text_color = "Primary"
                MDSnackbar(MDSnackbarText(text=self.language_manager.get_text('history_link_loaded'))).open()
                if dialog:
                    dialog.dismiss()

            for link in reversed(history_list): # Show newest first
                items.append(
                    MDListItem(
                        MDListItemHeadlineText(Text=link),
                        on_release=lambda x, l=link: history_item_selected(l),
                    )
                )

            dialog = MDDialog(MDDialogHeadlineText(
                text=self.language_manager.get_text('history_title')),
                type="simple",
                items=items,
                size_hint=(0.9, 0.8) # Adjust size
            )
            dialog.open()

        except Exception as e:
            logging.error("MainViewMD: Error getting or displaying history: ",e)
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
        """Update texts for MDButtons, including those in nested layouts."""
        buttons_to_update = []
        for child in self.layout.walk():  # Use walk() to get all descendants
            if isinstance(child, MDButton):
                for subchild in child.children:
                    if isinstance(subchild, MDButtonText):
                        buttons_to_update.append((subchild, subchild.text))

        dict_data = self.language_manager.get_dict_lang()
        for button_text, original_text in buttons_to_update:
            if original_text in dict_data.values():
                for key, translated_text in dict_data.items():
                    if translated_text == original_text:
                        button_text.text = self.language_manager.get_text(key)
                        break  # Found the translation, move to the next button


    def _update_text_input_hints(self):
        """Update hint_texts for MDTextFields."""
        from kivy.clock import Clock
        hint_text_widgets = [
            child
            for child in self.layout.walk()
            if isinstance(child, MDTextFieldHintText)
        ]
        dict_data = self.language_manager.get_dict_lang()
        text_fields_to_refresh = []  # To store text fields that need refresh

        for hint_widget in hint_text_widgets:
            if hint_widget.text in dict_data.values():
                for key, translated_text in dict_data.items():
                    if translated_text == hint_widget.text:
                        print(
                            f"Updating hint_text '{hint_widget.text}'"
                            f" to '{self.language_manager.get_text(key)}'"
                        )
                        hint_widget.text = self.language_manager.get_text(key)
                        # Find the parent MDTextField to refresh it
                        text_field = hint_widget.parent
                        if text_field and text_field not in text_fields_to_refresh:
                            text_fields_to_refresh.append(text_field)
                        break

        # Force refresh after updating all hints
        def refresh_text_fields(*args):
            for field in text_fields_to_refresh:
                field.focus = True  # Give focus briefly
                field.focus = False  # Remove focus

        if text_fields_to_refresh:  # Only schedule if there are fields to refresh
            Clock.schedule_once(refresh_text_fields, 0)


    def _update_labels(self):
        """Update texts for MDLabels."""
        labels_to_update = []
        for child in self.layout.walk():
            if isinstance(child, MDLabel):
                labels_to_update.append((child, child.text))

        dict_data = self.language_manager.get_dict_lang()
        for label, original_text in labels_to_update:
            if original_text in dict_data.values():
                for key, translated_text in dict_data.items():
                    if translated_text == original_text:
                        #label.text = self.language_manager.get_text(key)
                        break


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

    