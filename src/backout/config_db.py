import json
import os
from typing import Dict, Any # Importa las anotaciones de tipo
from src.managers.ad_manager import AdManager
from src.managers.contact_manager import ContactManager
from src.managers.language_manager import LanguageManager
from src.managers.link_manager import LinkManager
from src.managers.history_manager import HistoryManager

def load_config(config_file: str) -> Dict[str, Any]:
    """
    Carga la configuración desde un archivo JSON.

    Args:
        config_file: La ruta al archivo de configuración JSON.

    Returns:
        Un diccionario con la configuración.  Retorna un diccionario vacío si el archivo no existe o hay un error al decodificar el JSON.
    """
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        return config.get("database", {})  # Devuelve un diccionario vacío si no se encuentra "database"
    except FileNotFoundError:
        print(f"Archivo de configuración no encontrado: {config_file}")
        return {}  # Devuelve un diccionario vacío si el archivo no existe
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON en {config_file}")
        return {}  # Devuelve un diccionario vacío si hay un error al decodificar JSON
    except Exception as e:
        print(f"Error inesperado al cargar la configuración: {e}")
        return {}

# Carga la configuración desde un archivo JSON
config_file_path = "config.json" # Define la ruta del archivo
db_config = load_config(config_file_path)

# Define valores por defecto si no están en el archivo de configuración o si el archivo no existe
DEFAULT_DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "$$18246308k",  # TODO: ¡Cambiar esto por una contraseña segura!
    "host": "localhost",
    "port": '5432',
}

# Actualiza el diccionario de configuración con los valores por defecto
db_config = {**DEFAULT_DB_CONFIG, **db_config}


# Inicialización de managers
managers = {
    'theme': None,
    'ad': AdManager(app_id="ca-app-pub-7788178322918855/5307920549"),
    'contact': ContactManager(),
    'language': LanguageManager(),
    'link': LinkManager(),
    'history': HistoryManager(**db_config)
}
