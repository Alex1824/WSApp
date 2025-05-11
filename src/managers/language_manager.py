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
                'premium_title': 'Upgrade to Premium',
                'error_phone_required':'Error Phone Required'
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
                'premium_title': 'Actualizar a Premium',
                'error_phone_required':'Error Telefono Requerido'
            },
            'Français': {
                'search_country':'Rechercher un pays',
                'enter_phone':'Entrez le numéro de téléphone',
                'paste_clipboard':'Coller depuis le Presse-papiers',
                'validate_link':'Valider et générer le lien',
                'copy_link':'Copier le lien dans le presse-papiers',
                'generated_link':'Le lien WhatsApp généré apparaîtra ici',
                'select_contact':'Sélectionnez parmi les contacts',
                'share_link':'Partager le lien',
                'go_premium':'Passez Premium',
                'premium_active':'Premium activé',
                'dark_mode':'Mode sombre',
                'light_mode':'Mode Lumière',
                'view_history':'historique',
                'close':'Fermer',
                'search_contacts':'Rechercher des contacts...',
                'custom_message':'Saisissez un message personnalisé (facultatif)',
                'phone_detected':'Numéro de téléphone détecté dans le presse-papiers. Souhaitez-vous l\'utiliser?',
                'clipboard_title':'Numéro de téléphone détecté',
                'country_detected':'Code de pays détecté',
                'yes':'Oui',
                'no':'Non',
                'premium_features':'Fonctionnalités premium',
                'auto_country':'Détection automatique du pays par GPS',
                'ip_detection':'Détection de pays par IP',
                'no_ads':'Pas de publicité',
                'buy_premium':'Acheter Premium',
                'cancel':'Annuler',
                'premium_title':'Passer à Premium',
                'error_phone_required':'Erreur Téléphone requis',
            }
        }
    
    def get_text(self, key):
        """Get translated text for a given key"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def get_dict_lang(self):
        return self.translations.get(self.last_language, {})
    
    def change_language(self, language):
        """Change the current language"""
        if language in list(self.translations.keys()):
            self.current_language = language
    
    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.translations.keys())