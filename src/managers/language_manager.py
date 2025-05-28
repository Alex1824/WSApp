from kivy.event import EventDispatcher
from kivy.properties import StringProperty

class LanguageManager(EventDispatcher):
    current_language = StringProperty('English')
    
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
                'error_phone_required':'Error Phone Required',
                'history_title': 'History',
                'history_empty': 'No links in history.',
                'use_clipboard_title': 'Use Clipboard',
                'use_clipboard_text': 'We detected a phone number in your clipboard. Would you like to use it?',
                'phone_number_hint': 'Phone number',
                'error_invalid_input': 'Invalid input',
                'link_copied': 'Link copied to clipboard',
                'error_no_link_to_copy': 'No generated link to copy',
                'error_no_contacts': 'No contacts found',
                'contact_selected': 'Contact selected',
                'error_contact_access': 'Error accessing contacts',
                'error_no_link_to_share': 'No generated link to share',
                'link_copied_share_failed': 'Could not share, link copied to clipboard',
                'link_copied_share_unavailable': 'Sharing not available, link copied',
                'premium_activated_success': 'Premium activated successfully',
                'error_opening_link': 'Error opening link',
                'history_link_loaded': 'History link loaded',
                'error_contact_permission_denied': 'Contact permission denied. Cannot select contacts.',
                # Additions from ERROR_MESSAGES:
                'empty_input': 'Phone number is required.',
                'invalid_format': 'Invalid phone number format',
                'parse_error': 'Error parsing phone number: {}',
                # 'detected_country' already exists, ensure its value is:
                # 'country_detected': 'Country Code Detected', # This seems to be the old one
                # New one from prompt is 'Detected country code: {}. Would you like to use it?'
                # The key 'country_detected' is different from 'detected_country'.
                # I will update 'country_detected' as it seems to be the one used for dialog titles
                # and add 'detected_country_message' for the specific format string.
                # Or, if 'country_detected' is meant to be the one with the format string, I'll update it.
                # Based on the example, 'detected_country' is the key for the format string.
                'detected_country': 'Detected country code: {}. Would you like to use it?',
                # Tooltip keys
                'copy_link_tooltip': 'Copy Link',
                'share_link_tooltip': 'Share Link',
                'select_contact_tooltip': 'Select Contact',
                'view_history_tooltip': 'View History',
                'go_premium_tooltip': 'Go Premium',
                'toggle_theme_tooltip': 'Toggle Theme'
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
                'error_phone_required':'Error Telefono Requerido',
                'history_title': 'Historial de Enlaces',
                'history_empty': 'No hay enlaces en el historial.',
                'use_clipboard_title': 'Usar Portapapeles',
                'use_clipboard_text': 'Hemos detectado un número de teléfono en tu portapapeles. ¿Te gustaría usarlo?',
                'phone_number_hint': 'Número de teléfono',
                'error_invalid_input': 'Entrada inválida',
                'link_copied': 'Enlace copiado al portapapeles',
                'error_no_link_to_copy': 'No hay enlace generado para copiar',
                'error_no_contacts': 'No se encontraron contactos',
                'contact_selected': 'Contacto seleccionado',
                'error_contact_access': 'Error al acceder a los contactos',
                'error_no_link_to_share': 'No hay enlace generado para compartir',
                'link_copied_share_failed': 'No se pudo compartir, enlace copiado al portapapeles',
                'link_copied_share_unavailable': 'Compartir no disponible, enlace copiado',
                'premium_activated_success': 'Premium activado con éxito',
                'error_opening_link': 'Error al abrir el enlace',
                'history_link_loaded': 'Enlace del historial cargado',
                'error_contact_permission_denied': 'Permiso de contactos denegado. No se pueden seleccionar contactos.',
                # Additions from ERROR_MESSAGES:
                'empty_input': 'El número de teléfono es obligatorio.',
                'invalid_format': 'Formato de número de teléfono inválido',
                'parse_error': 'Error al analizar el número de teléfono: {}',
                # 'detected_country' already exists, ensure its value is:
                'detected_country': 'Código de país detectado: {}. ¿Te gustaría usarlo?',
                # Tooltip keys
                'copy_link_tooltip': 'Copiar Enlace',
                'share_link_tooltip': 'Compartir Enlace',
                'select_contact_tooltip': 'Seleccionar Contacto',
                'view_history_tooltip': 'Ver Historial',
                'go_premium_tooltip': 'Hazte Premium',
                'toggle_theme_tooltip': 'Cambiar Tema'
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
                'history_title': 'Historique des liens',
                'history_empty': "Aucun lien dans l'historique.",
                'use_clipboard_title': 'Utiliser le Presse-papiers',
                'use_clipboard_text': "Nous avons détecté un numéro de téléphone dans votre presse-papiers. Voulez-vous l'utiliser ?",
                'phone_number_hint': 'Numéro de téléphone',
                'error_invalid_input': 'Entrée invalide',
                'link_copied': 'Lien copié dans le presse-papiers',
                'error_no_link_to_copy': 'Aucun lien généré à copier',
                'error_no_contacts': 'Aucun contact trouvé',
                'contact_selected': 'Contact sélectionné',
                'error_contact_access': "Erreur d'accès aux contacts",
                'error_no_link_to_share': 'Aucun lien généré à partager',
                'link_copied_share_failed': 'Impossible de partager, lien copié dans le presse-papiers',
                'link_copied_share_unavailable': 'Partage non disponible, lien copié',
                'premium_activated_success': 'Premium activé avec succès',
                'error_opening_link': "Erreur lors de l'ouverture du lien",
                'history_link_loaded': "Lien de l'historique chargé",
                'error_contact_permission_denied': "Autorisation d'accès aux contacts refusée. Impossible de sélectionner des contacts.",
                # Additions from ERROR_MESSAGES:
                'empty_input': 'Le numéro de téléphone est requis.',
                'invalid_format': 'Format de numéro de téléphone invalide',
                'parse_error': "Erreur lors de l'analyse du numéro de téléphone: {}",
                # 'detected_country' already exists, ensure its value is:
                'detected_country': "Code pays détecté: {}. Souhaitez-vous l'utiliser?",
                # Tooltip keys
                'copy_link_tooltip': 'Copier le lien',
                'share_link_tooltip': 'Partager le lien',
                'select_contact_tooltip': 'Sélectionner un contact',
                'view_history_tooltip': "Voir l'historique",
                'go_premium_tooltip': 'Passez Premium',
                'toggle_theme_tooltip': 'Changer de thème'
            }
        }
    
    def get_text(self, key):
        """Get translated text for a given key"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def change_language(self, language):
        """Change the current language"""
        if language in list(self.translations.keys()):
            self.current_language = language
    
    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.translations.keys())