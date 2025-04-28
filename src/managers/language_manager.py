from kivy.event import EventDispatcher
from kivy.properties import StringProperty

class LanguageManager(EventDispatcher):
    current_language = StringProperty('English')
    last_language = StringProperty('English')
    
    def __init__(self):
        super().__init__()
        self.translations = {
            'English': {
                'search_country': 'Search country',
                'enter_phone': 'Enter phone number',
                'paste_clipboard': 'Paste from Clipboard',
                'validate_link': 'Validate and Generate Link',
                'copy_link': 'Copy Link to Clipboard',
                'generated_link': 'Generated WhatsApp link will appear here',
                'select_contact': 'Select from Contacts',
                'share_link': 'Share Link',
                'go_premium': 'Go Premium',
                'premium_active': 'Premium Activated',
                'dark_mode': 'Dark Mode',
                'light_mode': 'Light Mode',
                'view_history': 'View History',
                'close': 'Close',
                'search_contacts': 'Search contacts...',
                'custom_message': 'Enter custom message (optional)',
                'phone_detected': 'Phone number detected in clipboard. Would you like to use it?',
                'clipboard_title': 'Phone Number Detected',
                'country_detected': 'Country Code Detected',
                'yes': 'Yes',
                'no': 'No',
                'premium_features': 'Premium Features:',
                'auto_country': 'Automatic country detection by GPS',
                'ip_detection': 'Country detection by IP',
                'no_ads': 'No advertisements',
                'buy_premium': 'Buy Premium',
                'cancel': 'Cancel',
                'premium_title': 'Upgrade to Premium'
            },
            'Español': {
                'search_country': 'Buscar país',
                'enter_phone': 'Ingrese número de teléfono',
                'paste_clipboard': 'Pegar desde el portapapeles',
                'validate_link': 'Validar y Generar Enlace',
                'copy_link': 'Copiar Enlace al Portapapeles',
                'generated_link': 'El enlace de WhatsApp generado aparecerá aquí',
                'select_contact': 'Seleccionar de Contactos',
                'share_link': 'Compartir Enlace',
                'go_premium': 'Versión Premium',
                'premium_active': 'Premium Activado',
                'dark_mode': 'Modo Oscuro',
                'light_mode': 'Modo Claro',
                'view_history': 'Ver Historial',
                'close': 'Cerrar',
                'search_contacts': 'Buscar contactos...',
                'custom_message': 'Ingrese mensaje personalizado (opcional)',
                'phone_detected': 'Número de teléfono detectado en el portapapeles. ¿Desea utilizarlo?',
                'clipboard_title': 'Número Telefónico Detectado',
                'country_detected': 'Código de País Detectado',
                'yes': 'Sí',
                'no': 'No',
                'premium_features': 'Características Premium:',
                'auto_country': 'Detección automática de país por GPS',
                'ip_detection': 'Detección de país por IP',
                'no_ads': 'Sin publicidad',
                'buy_premium': 'Comprar Premium',
                'cancel': 'Cancelar',
                'premium_title': 'Actualizar a Premium'
            },
            'Français': {
                'search_country': 'Rechercher un pays',
                'enter_phone': 'Entrez le numéro de téléphone',
                'paste_clipboard': 'Coller depuis le presse-papiers',
                'validate_link': 'Valider et Générer le Lien',
                'copy_link': 'Copier le Lien dans le Presse-papiers',
                'generated_link': 'Le lien WhatsApp généré apparaîtra ici',
                'select_contact': 'Sélectionner dans les Contacts',
                'share_link': 'Partager le Lien',
                'go_premium': 'Version Premium',
                'premium_active': 'Premium Activé',
                'dark_mode': 'Mode Sombre',
                'light_mode': 'Mode Clair',
                'view_history': 'Voir Historique',
                'close': 'Fermer',
                'search_contacts': 'Rechercher des contacts...',
                'custom_message': 'Entrez un message personnalisé (facultatif)',
                'phone_detected': 'Numéro de téléphone détecté dans le presse-papiers. Voulez-vous l\'utiliser?',
                'clipboard_title': 'Numéro de Téléphone Détecté',
                'country_detected': 'Code Pays Détecté',
                'yes': 'Oui',
                'no': 'Non'
            }
        }
    
    def get_text(self, key):
        """Get translated text for a given key"""
        return self.translations.get(self.current_language, {}).get(key, key)
    def get_keys(self):
        return self.translations.get(self.last_language, {})
    
    def change_language(self, language):
        """Change the current language"""
        self.last_language = self.current_language
        if language in list(self.translations.keys()):
            self.current_language = language
    
    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.translations.keys())