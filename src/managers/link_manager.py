from kivy.event import EventDispatcher
from kivy.properties import StringProperty, BooleanProperty
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.logger import Logger
from ..core.phone_utils import validate_number, clean_number, get_error_message, is_valid_phone_format
from src.managers.history_manager import HistoryManager as HM

class LinkManager(EventDispatcher):
    current_link = StringProperty('')
    is_valid_clipboard = BooleanProperty(False)
    last_clipboard = StringProperty('')
    
    def __init__(self, language_manager): # Added language_manager
        super().__init__()
        self.language_manager = language_manager # Store language_manager
        # Bind to window focus events instead of using Clock
        Window.bind(on_restore=self.check_clipboard)
        Window.bind(on_resume=self.check_clipboard)
        
    def check_clipboard(self, *args):
        """Check clipboard content when app becomes active"""
        try:
            content = Clipboard.paste()
            if content and content != self.last_clipboard and len(content) > 8:
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
            # validate_number will return 'empty_input' key, let it handle that
            # and then translate the key here.
            # This specific check can be removed if validate_number handles it robustly.
            # For now, keeping it as per original logic flow but using new LM.
            return False, self.language_manager.get_text('empty_input')
            
        # Validate and format the number
        # validate_number now returns:
        # (validated_number_string, None) on success
        # (None, message_key_or_preformatted_message_string) on failure or with info
        validated_number, result_message = validate_number(phone_number, country_code, self.language_manager)
        
        if validated_number:
            # Remove the '+' from the validated number as wa.me links don't use it
            final_number_for_link = validated_number.lstrip('+')
            if custom_message:
                self.current_link = f"https://wa.me/{final_number_for_link}?text={custom_message.replace(' ', '%20')}"
            else:
                self.current_link = f"https://wa.me/{final_number_for_link}"

            # If validate_number returned a message (e.g. "detected_country"),
            # it's already formatted by phone_utils.
            # This message is informational, not an error.
            if result_message: 
                return True, (self.current_link, result_message) # Pass the formatted message as is
            return True, self.current_link # Success, no special message
        else:
            # An error occurred, result_message is either a key or a pre-formatted string
            self.current_link = ''
            # Check if result_message is one of the keys that phone_utils might return directly
            # (like 'empty_input', 'invalid_format')
            # or if it's already formatted (like for 'parse_error', 'detected_country').
            # For simplicity here, we assume LinkManager is responsible for final translation if it's a key.
            # However, phone_utils was designed to return formatted messages for 'parse_error' and 'detected_country'.
            # So, if result_message contains '{}' or specific country code, it's likely pre-formatted.
            # Otherwise, it's a key.
            
            # The keys returned by validate_number are 'empty_input', 'invalid_format'.
            # The pre-formatted messages are for 'parse_error' and 'detected_country'.
            # Since validated_number is None here, 'detected_country' won't be the case.
            # So, result_message is either 'empty_input', 'invalid_format', or a formatted 'parse_error'.
            
            if result_message in ['empty_input', 'invalid_format']:
                 return False, self.language_manager.get_text(result_message)
            return False, result_message # Return pre-formatted 'parse_error' or other direct messages
            
    def clean_phone_number(self, number):
        """Clean and validate phone number format"""
        if not number:
            return None
        return clean_number(number)
        
    # Removed set_language method