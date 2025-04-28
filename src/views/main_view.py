from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDIcon
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from src.ui.ui_manager import UIManager
from logging import Logger
from kivymd.uix.snackbar import MDSnackbar
from kivy.core.clipboard import Clipboard
from kivymd.uix.list import MDListItem
from kivymd.uix.label import MDLabel

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
        
        # Bind to clipboard changes
        self.link_manager.bind(is_valid_clipboard=self.on_valid_clipboard)
        
        self.setup_ui()
        
    def setup_ui(self):
        
        self.theme_cls.theme_style = "Light"  # o "Dark"
        self.theme_cls.primary_palette = "Teal"  # Puedes cambiar a "Blue", "Red", etc.
        self.theme_cls.material_style = "M3"  # Usar Material Design 3
        
        # Layout principal
        main_box = MDBoxLayout(
            orientation="vertical",
            spacing=15, 
            padding=20)
        
        # Scrollable content
        scroll_view = MDScrollView()
        self.layout = MDGridLayout(
            cols=1,
            spacing=15,
            size_hint_y=None,
            adaptive_height=True,
            padding=20
            )
        
        # Logo
        logo = MDIcon(
            source='assets/images/logo.png',
            #size_hint=(1, None),
            #height=dp(100),
            #pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(logo)
        
        # Language selector (ahora como dropdown)
    
        self.language_button = self.ui_manager.create_button(
            text=self.language_manager.current_language,
            icon="translate",
            style="outlined",
            callback=self.show_language_menu
        )
        self.layout.add_widget(self.language_button)
        
        # Phone input section
        self.setup_phone_input()
        
        # Action buttons
        self.setup_action_buttons()
        
        # Link display
        self.link_button = self.ui_manager.create_hyperlink_button(
            text=self.language_manager.get_text('generated_link'),
            on_press=self.on_link_press
        )
        self.layout.add_widget(self.link_button)
        
        scroll_view.add_widget(self.layout)
        main_box.add_widget(scroll_view)
        self.add_widget(main_box)
        
    def setup_phone_input(self):
        from ..core.phone_utils import get_country_code_by_location, get_country_flag
        
        # Country selection
        country_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50), spacing=10)
        
        self.country_filter = self.ui_manager.create_text_input(
            hint_text=self.language_manager.get_text('search_country'),
            size_hint=(0.8, None),
            height=dp(50)
        )
        
        self.flag_label = MDButton(
            MDButtonText(
                text="",
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1)
            ),
            style="text",
            size_hint=(0.2, None),
            height=dp(50),
            #font_size='24sp'
        )
        
        # Auto-detect country if premium
        if self.is_premium:
            detected_country = get_country_code_by_location()
            if detected_country:
                self.country_filter.text = detected_country
                self.flag_label.children[0].text = get_country_flag(detected_country)
        
        self.country_filter.bind(
            text=lambda instance, value: self.update_flag(value)
        )
        
        country_box.add_widget(self.country_filter)
        country_box.add_widget(self.flag_label)
        self.layout.add_widget(country_box)
        
        # Phone number input
        self.phone_input = self.ui_manager.create_text_input(
            hint_text=self.language_manager.get_text('enter_phone')
        )
        self.layout.add_widget(self.phone_input)
        
        # Custom message input
        self.message_input = self.ui_manager.create_text_input(
            hint_text=self.language_manager.get_text('custom_message'),
            multiline=True
        )
        self.layout.add_widget(self.message_input)
    
    def update_flag(self, country_code):
        from ..core.phone_utils import get_country_flag
        if country_code and len(country_code) >= 2:
            self.flag_label.children[0].text = get_country_flag(country_code[:2])
        else:
            self.flag_label.children[0].text = ""
            
    def setup_action_buttons(self):
        buttons = [
            ('validate_link', self.on_validate, "filled", (0.8, 0.2, 0.2, 1), "check"),
            ('copy_link', self.on_copy, "elevated", (0.2, 0.6, 0.8, 1), "content-copy"),
            ('select_contact', self.on_select_contact, "tonal", None, "account-box"),
            ('share_link', self.on_share, "elevated", None, "share-variant"),
            ('go_premium', self.on_premium, "filled", (0.8, 0.8, 0.2, 1), "crown"),
            ('dark_mode', self.on_theme_toggle, "outlined", None, "theme-light-dark"),
            ('view_history', self.on_history, "tonal", None, "history")
        ]
        
        for text_key, callback, style, bg_color, icon in buttons:
            btn = self.ui_manager.create_button(
                text=self.language_manager.get_text(text_key),
                callback=callback,
                style=style,
                bg_color=bg_color,
                icon=icon
            )
            self.layout.add_widget(btn)
            
    def show_language_menu(self, instance):
        languages = [
            {
                "text": lang,
                "on_release": lambda x=lang: self.on_language_change(x)
            } for lang in self.language_manager.get_available_languages()
        ]
        print(languages[0]['on_release'])
        self.language_dropdown = self.ui_manager.create_dropdown(
            caller=instance,
            options=languages,
            callback=None
        )
        self.language_dropdown.open()
    
        
    def on_language_change(self, language):
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
        if not self.phone_input.text:
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
        """Show dialog when country code is detected/guessed"""
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
            MDSnackbar(text=self.language_manager.get_text('link_copied')).open()
            # AnimationManager.button_press(instance) # Adapt/replace
        else:
             MDSnackbar(text=self.language_manager.get_text('error_no_link_to_copy')).open()

    def on_select_contact(self, instance):
        """Show contact selection dialog"""
        # Needs replacement for ContactsPopup using KivyMD components
        # Example using a simple MDDialog with a list (requires contact_manager)
        try:
            contacts = self.contact_manager.get_contacts() # [{'name': 'John', 'number': '123'}, ...]
            if not contacts:
                MDSnackbar(text=self.language_manager.get_text('error_no_contacts')).open()
                return

            # Create list items for the dialog
            # Using kivymd.uix.list.OneLineAvatarIconListItem would be better if icons/avatars are available
            items = []
            dialog = None # Define dialog first

            def contact_selected_callback(contact_number, contact_name):
                 self.phone_input.text = contact_number
                 MDSnackbar(text=self.language_manager.get_text('contact_selected') + f": {contact_name}").open()
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
            MDSnackbar(text=self.language_manager.get_text('error_contact_access')).open()


    def on_share(self, instance):
        """Share the generated link"""
        if not self.generated_link_text:
            MDSnackbar(text=self.language_manager.get_text('error_no_link_to_share')).open()
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
                    current_activity = self.app.AndroidActivity
                    if current_activity:
                        current_activity.startActivity(chooser)
                    else:
                         Logger.error("Could not get Android activity reference.")
                         Clipboard.copy(link_to_share) # Fallback to copy
                         MDSnackbar(text=self.language_manager.get_text('link_copied_share_failed')).open()

                except Exception as e:
                    Logger.error(f'Error sharing link on Android: {str(e)}')
                    Clipboard.copy(link_to_share) # Fallback to copy
                    MDSnackbar(text=self.language_manager.get_text('link_copied_share_failed')).open()
            else: # Other platforms (iOS, Desktop) - Copy to clipboard
                Clipboard.copy(link_to_share)
                MDSnackbar(text=self.language_manager.get_text('link_copied_share_unavailable')).open()
        except Exception as e:
             Logger.error(f'Error using Plyer share: {str(e)}')
             Clipboard.copy(link_to_share) # Fallback to copy
             MDSnackbar(text=self.language_manager.get_text('link_copied_share_failed')).open()

    def on_premium(self, instance):
        """Show premium purchase dialog or indicate premium status"""
        if not self.is_premium:
            # --- Show Premium Purchase Dialog ---
            dialog = None # Define dialog variable first

            # Content for the dialog (Using MDLabel for features)
            features_box = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing=dp(5))
            features_box.add_widget(MDLabel(text="✓ " + self.language_manager.get_text('auto_country'), adaptive_height=True, theme_text_color="Secondary"))
            features_box.add_widget(MDLabel(text="✓ " + self.language_manager.get_text('ip_detection'), adaptive_height=True, theme_text_color="Secondary"))
            features_box.add_widget(MDLabel(text="✓ " + self.language_manager.get_text('no_ads'), adaptive_height=True, theme_text_color="Secondary"))


            buy_btn = MDButton(
                text=self.language_manager.get_text('buy_premium'),
                theme_text_color="Custom",
                text_color=self.app.theme_cls.primary_color, # Use theme color
                on_press=lambda *args: (self._activate_premium(), dialog.dismiss())
            )
            cancel_btn = MDButton(
                text=self.language_manager.get_text('cancel'),
                 on_press=lambda *args: dialog.dismiss()
            )

            dialog = MDDialog(
                title=self.language_manager.get_text('premium_title'),
                text=self.language_manager.get_text('premium_features'), # Main description
                # type="custom", # If adding custom content widget
                # content_cls=features_box, # Use this if type="custom"
                buttons=[cancel_btn, buy_btn],
                size_hint=(0.9, None),
                height=dp(280) # Adjust height
            )
            # If using type="custom", add the features box *after* creating dialog
            # dialog.content_cls.add_widget(features_box) # Add features list

            dialog.open()
        else:
            # Already premium - show a MDSnackbar message
            MDSnackbar(text=self.language_manager.get_text('premium_already_active')).open()


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

        MDSnackbar(text=self.language_manager.get_text('premium_activated_success')).open()


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
        current_style = self.app.theme_cls.theme_style
        if current_style == "Light":
            self.app.theme_cls.theme_style = "Dark"
        else:
            self.app.theme_cls.theme_style = "Light"
        # Update button text immediately (or refactor update_texts to handle this)
        self.update_texts() # Call update_texts to refresh button labels
        # AnimationManager.button_press(instance) # Adapt/replace

    def on_history(self, instance):
        """Show history dialog"""
        # Needs replacement for HistoryPopup using KivyMD components
        try:
            history_list = self.history_manager.get_history() # Assume returns list of strings (links)
            if not history_list:
                 MDSnackbar(text=self.language_manager.get_text('history_empty')).open()
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
                MDSnackbar(text=self.language_manager.get_text('history_link_loaded')).open()
                if dialog:
                    dialog.dismiss()

            for link in reversed(history_list): # Show newest first
                 items.append(
                     MDListItem(
                         text=link,
                         on_release=lambda x, l=link: history_item_selected(l)
                     )
                 )

            dialog = MDDialog(
                 title=self.language_manager.get_text('history_title'),
                 type="simple",
                 items=items,
                 size_hint=(0.9, 0.8) # Adjust size
            )
            dialog.open()

        except Exception as e:
            Logger.error(f"MainViewMD: Error getting or displaying history: {e}")
            MDSnackbar(text=self.language_manager.get_text('error_history_access')).open()


    def on_link_press(self, instance):
        """Handle link button press - open in browser"""
        if self.generated_link_text:
            try:
                from webbrowser import open as open_url
                open_url(self.generated_link_text)
            except Exception as e:
                 Logger.error(f"Failed to open link: {e}")
                 MDSnackbar(text=self.language_manager.get_text('error_opening_link')).open()


    def update_texts(self):
        """Update all UI texts based on current language"""
        self.country_filter.hint_text = self.language_manager.get_text('search_country')
        self.phone_input.hint_text = self.language_manager.get_text('enter_phone')
        self.message_input.hint_text = self.language_manager.get_text('custom_message')
        
        child=  [
            (subchild.text,subchild)
            for child in self.layout.children 
            if isinstance(child, MDButton)
            for subchild in child.children 
            if isinstance(subchild, MDButtonText)
]
        dict_data = {}
        for key, value in child:
            dict_data[key] = value

        #print(dict_data)
            #if hasattr(child, 'children') and len(child.children) > 1:
        # for i in len(child):  
        #     if isinstance(child[i].children[0], MDButtonText):
        #         values=child.children[0].append()
        #         print(values)
        for key, VA in dict_data.items():
            print(key, VA)
        print(self.language_manager.get_keys())