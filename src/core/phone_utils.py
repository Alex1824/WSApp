import re
import phonenumbers
import pycountry
from emoji import emojize
import requests
import geocoder
from functools import lru_cache
from phonenumbers.phonenumberutil import region_code_for_country_code
from kivy.core.clipboard import Clipboard

# ERROR_MESSAGES dictionary and get_error_message function are removed.

def detect_country_code_from_number(number):
    """Try to detect country code from the phone number itself"""
    try:
        # Remove any non-digit characters except '+'
        cleaned = re.sub(r'[^\d+]', '', number)
        if cleaned.startswith('+'):
            parsed = phonenumbers.parse(cleaned)
            if phonenumbers.is_valid_number(parsed):
                return str(parsed.country_code)
    except:
        pass
    return None

def is_valid_phone_format(number):
    """Check if a string appears to be a phone number"""
    # Remove common phone number formatting characters
    cleaned = re.sub(r'[-\s.()\[\]]', '', number)
    # Check if it's mostly digits (allowing + at start)
    if cleaned.startswith('+'):
        cleaned = cleaned[1:]
    return cleaned.isdigit() and 8 <= len(cleaned) <= 15

def validate_number(raw_number, country_code='', language_manager=None):
    """Validate a phone number with improved detection"""
    if language_manager is None:
        # Fallback or error if language_manager is not provided
        # For this task, we'll assume it's always provided.
        # If not, one might raise ValueError("language_manager is required")
        # or return a default English message key directly.
        # For now, to avoid breaking execution if accidentally not passed:
        print("Warning: language_manager not provided to validate_number. Using message keys directly.")
        fallback_get_text = lambda key, *args: key if not args else key.format(*args)
    else:
        fallback_get_text = lambda key, *args: language_manager.get_text(key) if not args else language_manager.get_text(key).format(*args)

    try:
        if not raw_number:
            return None, 'empty_input' # Return key
            
        # First check if it's even a phone number format
        if not is_valid_phone_format(raw_number):
            return None, 'invalid_format' # Return key
            
        # Try to clean and format the number
        cleaned_number = clean_number(raw_number, country_code)
        if not cleaned_number:
            return None, 'invalid_format' # Return key

        # Parse and validate the number
        parsed_number = phonenumbers.parse(cleaned_number)
        if phonenumbers.is_valid_number(parsed_number):
            formatted = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            detected_country_alpha2 = phonenumbers.region_code_for_number(parsed_number)
            # The 'detected_country' key expects the country code as a format argument.
            # The message should be formatted here as it includes a parameter.
            if not country_code: # If country_code was not initially provided by user
                # This message is now pre-formatted by phone_utils
                return formatted, fallback_get_text('detected_country', detected_country_alpha2)
            return formatted, None # Success, no message
        else:
            return None, 'invalid_format' # Return key
    except phonenumbers.NumberParseException as e:
        # This message is also pre-formatted by phone_utils
        return None, fallback_get_text('parse_error', str(e))


def clean_number(raw_number, country_code=''):
    """Clean and format a phone number with improved country code detection"""
    try:
        # Remove any non-digit characters except '+'
        number = re.sub(r'[^\d+]', '', raw_number)
        
        # Si el número ya tiene +, asumimos que incluye el código de país
        if number.startswith('+'):
            # Validar que el número con + tiene una longitud razonable
            if 8 <= len(number) <= 15:
                return number
            return None
            
        # Si se proporciona código de país, asegurarse de que tenga el formato correcto
        if country_code:
            # Limpiar el código de país
            clean_country = country_code.strip().lstrip('+')
            if clean_country.isdigit():
                # Asegurarse de que el número no empiece ya con el código de país
                if not number.startswith(clean_country):
                    return f"+{clean_country}{number}"
                return f"+{number}"
            
        # Si no hay código de país válido, intentar detectarlo por ubicación
        detected_code = get_country_code_by_location()
        if detected_code:
            detected_code = detected_code.lstrip('+')
            if not number.startswith(detected_code):
                return f"+{detected_code}{number}"
            return f"+{number}"
                
        return None
    except Exception as e:
        print(f"Error cleaning number: {e}")
        return None

def get_country_list():
    country_list = []
    print("Generating country list...")
    for country in pycountry.countries:
        try:
            flag = emojize(f":{country.alpha_2.lower()}:")
            country_list.append(f"{flag} {country.name} (+{get_country_code_by_alpha2(country.alpha_2)})")
        except KeyError as e:
            print(f"Error processing country {country.name}: {e}")
    return country_list

def get_country_code_by_alpha2(alpha2):
    try:
        return str(phonenumbers.country_code_for_region(alpha2)) or ''
    except Exception as e:
        print(f"Error getting country code for {alpha2}: {e}")
        return ''

def get_country_code():
    try:
        response = requests.get('https://ipinfo.io', timeout=5)
        data = response.json()
        country = data.get('country', 'US')
        return f"+{get_country_code_by_alpha2(country)}"
    except requests.RequestException as e:
        print(f"Error fetching country code: {e}")
        return ''

@lru_cache(maxsize=100)
def get_country_flag(country_code: str) -> str:
    """
    Convierte el código de país ISO 3166-1 alfa-2 en un emoji de bandera.
    Ejemplo: 'US' → '🇺🇸'
    """
    if not country_code or not isinstance(country_code, str) or len(country_code) != 2:
        return ""  # bandera blanca por defecto para errores

    try:
        country_code = country_code.upper()
        base = ord('🇦') - ord('A')
        return chr(ord(country_code[0]) + base) + chr(ord(country_code[1]) + base)
    except Exception as e:
        print(f"Error generating flag for {country_code}: {e}")
        return ""

def get_country_code_by_location():
    """
    Obtiene el código de país basado en la ubicación GPS (característica premium)
    """
    try:
        g = geocoder.ip('me')
        if g.ok:
            return g.country
    except Exception:
        pass
    return None

def get_country_code_by_ip():
    """
    Obtiene el código de país basado en la IP (característica premium)
    """
    try:
        response = requests.get('https://ipapi.co/json/')
        if response.status_code == 200:
            data = response.json()
            return data.get('country_code')
    except Exception:
        pass
    return None

def is_premium_feature_enabled(is_premium):
    """Verifica si las características premium están habilitadas"""
    return is_premium

# Added advanced validation using an external API
def validate_number_advanced(phone_number, country_code):
    api_url = "https://api.example.com/validate"
    params = {
        "phone": phone_number,
        "country_code": country_code
    }
    try:
        response = requests.get(api_url, params=params, timeout=5)
    except requests.RequestException as e:
        return False, f"Error during validation request: {str(e)}"
    if response.status_code == 200:
        data = response.json()
        return data.get("is_valid", False), data.get("message", "Invalid number")
    else:
        return False, "Validation service unavailable"