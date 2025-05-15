import psycopg2
import os

class HistoryManager:
    def __init__(self, dbname, user, password, host, port):
        """
        Inicializa el administrador de la base de datos PostgreSQL.

        Args:
            dbname (str): Nombre de la base de datos.
            user (str): Nombre de usuario de la base de datos.
            password (str): Contraseña de la base de datos.
            host (str): Host del servidor de la base de datos.
            port (int): Puerto del servidor de la base de datos.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_table()

    def _connect(self):
        """Establece la conexión a la base de datos PostgreSQL."""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos PostgreSQL: {e}")
            raise  # Re-lanzar la excepción para que se maneje en el nivel superior

    def _create_table(self):
        """Crea la tabla de historial si no existe."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id SERIAL PRIMARY KEY,  -- Usamos SERIAL para el autoincremento en PostgreSQL
                    link TEXT NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error al crear la tabla en PostgreSQL: {e}")
            raise

    def add_link(self, link, notes=""):
        """
        Agrega un enlace al historial.

        Args:
            link (str): El enlace de WhatsApp a agregar.
            notes (str, optional): Información adicional proporcionada por el usuario. Por defecto es "".

        Returns:
            bool: True si el enlace se agregó con éxito, False en caso contrario.
        """
        try:
            self._connect()
            self.cursor.execute("INSERT INTO history (link, notes) VALUES (%s, %s)", (link, notes))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error al agregar enlace al historial en PostgreSQL: {e}")
            self.conn.rollback()  # Importante: Revertir la transacción en caso de error
            return False
        finally:
            self._close()

    def get_history(self):
        """
        Obtiene el historial de enlaces.

        Returns:
            list: Una lista de tuplas, donde cada tupla contiene (link, notes, created_at).
                Retorna una lista vacía en caso de error.
        """
        try:
            self._connect()
            self.cursor.execute("SELECT link, notes, created_at FROM history ORDER BY created_at DESC")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al obtener el historial de PostgreSQL: {e}")
            return []
        finally:
            self._close()

    def clear_history(self):
        """Elimina todo el historial."""
        try:
            self._connect()
            self.cursor.execute("DELETE FROM history")
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error al eliminar el historial en PostgreSQL: {e}")
            self.conn.rollback()
            return False
        finally:
            self._close()

    def _close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def __del__(self):
        """Cierra la conexión a la base de datos al destruir el objeto."""
        self._close()

# Ejemplo de uso:
if __name__ == '__main__':
    try:
        # Configura tus credenciales de la base de datos
        db_name = os.environ.get('DB_NAME', 'your_db_name')
        db_user = os.environ.get('DB_USER', 'your_db_user')
        db_password = os.environ.get('DB_PASSWORD', 'your_db_password')
        db_host = os.environ.get('DB_HOST', 'your_db_host')
        db_port = int(os.environ.get('DB_PORT', '5432'))

        history_manager = HistoryManager(db_name, db_user, db_password, db_host, db_port)

        # Agregar un enlace
        history_manager.add_link("https://www.ejemplo.com", "Este es un ejemplo")

        # Obtener el historial
        history = history_manager.get_history()
        for row in history:
            print(row)

        # Limpiar el historial
        history_manager.clear_history()

    except psycopg2.Error as e:
        print(f"Error general de PostgreSQL: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")