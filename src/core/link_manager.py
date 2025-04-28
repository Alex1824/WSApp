from kivy.event import EventDispatcher
from kivy.properties import StringProperty, BooleanProperty
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.logger import Logger
from ..core.phone_utils import validate_number, clean_number, get_error_message, is_valid_phone_format

class LinkManager(EventDispatcher):
    current_link = StringProperty('')
    is_valid_clipboard = BooleanProperty(False)
    last_clipboard = StringProperty('')
    
    def __init__(self):
        super().__init__()
        self.current_language = 'English'
        # Bind to window focus events instead of using Clock
        Window.bind(on_restore=self.check_clipboard)
        Window.bind(on_resume=self.check_clipboard)
        
    def check_clipboard(self, *args):
        """Check clipboard content when app becomes active"""
        try:
            content = Clipboard.paste()
            if content and content != self.last_clipboard:
                self.last_clipboard = content
                self.is_valid_clipboard = is_valid_phone_format(content)
                Logger.debug('LinkManager: Clipboard checked on app restore/resume')
                return True
        except Exception as e:
            Logger.error(f'LinkManager: Error checking clipboard: {str(e)}')
        return False
        
    def generate_link(self, phone_number, country_code='', custom_message=''):
        """Generate a WhatsApp link with validation"""
        if not phone_number:
            return False, get_error_message('empty_input', self.current_language)
            
        # Validate and format the number
        validated_number, message = validate_number(phone_number, country_code, self.current_language)
        
        if validated_number:
            # Remove the '+' from the validated number as wa.me links don't use it
            validated_number = validated_number.lstrip('+')
            if custom_message:
                self.current_link = f"https://wa.me/{validated_number}?text={custom_message.replace(' ', '%20')}"
            else:
                self.current_link = f"https://wa.me/{validated_number}"
                
            # Si hay un mensaje sobre código de país detectado, retornarlo con el link
            if message and 'detected_country' in message:
                return True, (self.current_link, message)
            return True, self.current_link
        else:
            self.current_link = ''
            return False, message
            
    def clean_phone_number(self, number):
        """Clean and validate phone number format"""
        if not number:
            return None
        return clean_number(number)
        
    def set_language(self, language):
        """Set the current language for error messages"""
        self.current_language = language