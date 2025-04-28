from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp
from .ui_manager import UIManager
from .animation_manager import AnimationManager

class ContactsPopup:
    @staticmethod
    def create(contacts, on_select, language_manager):
        """Create a popup for contacts selection"""
        popup = Popup(
            title=language_manager.get_text('select_contact'),
            size_hint=(0.9, 0.9)
        )
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Search input
        search_input = UIManager.create_text_input(
            hint_text=language_manager.get_text('search_contacts')
        )
        layout.add_widget(search_input)
        
        # Scrollable contact list
        scroll = ScrollView(size_hint=(1, 1))
        contact_layout = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None
        )
        contact_layout.bind(minimum_height=contact_layout.setter('height'))
        
        def on_contact_press(contact):
            on_select(contact)
            popup.dismiss()
        
        # Populate contacts
        for contact in contacts:
            btn = UIManager.create_styled_button(
                text=f"{contact['name']}\n{contact['number']}",
                callback=lambda c=contact: on_contact_press(c)
            )
            contact_layout.add_widget(btn)
        
        scroll.add_widget(contact_layout)
        layout.add_widget(scroll)
        
        # Close button
        close_button = UIManager.create_styled_button(
            text=language_manager.get_text('close'),
            callback=popup.dismiss
        )
        layout.add_widget(close_button)
        
        popup.content = layout
        return popup

class HistoryPopup:
    @staticmethod
    def create(history, language_manager):
        """Create a popup for viewing history"""
        popup = Popup(
            title=language_manager.get_text('view_history'),
            size_hint=(0.8, 0.8)
        )
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Create scrollable history list
        scroll = ScrollView(size_hint=(1, 1))
        history_layout = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None
        )
        history_layout.bind(minimum_height=history_layout.setter('height'))
        
        for link in history:
            link_btn = UIManager.create_hyperlink_button(text=link)
            AnimationManager.fade_in(link_btn)
            history_layout.add_widget(link_btn)
        
        scroll.add_widget(history_layout)
        layout.add_widget(scroll)
        
        # Close button
        close_button = UIManager.create_styled_button(
            text=language_manager.get_text('close'),
            callback=popup.dismiss
        )
        layout.add_widget(close_button)
        
        popup.content = layout
        return popup