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
        self._connect()  # Initial connection
        if self.conn: # Only create table if connection was successful
            self._create_table()

    def _connect(self):
        """Establece la conexión a la base de datos PostgreSQL."""
        # Close existing connection if any before creating a new one
        if self.conn and not self.conn.closed:
            self._close()
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
            self.conn = None # Ensure conn is None if connection failed
            self.cursor = None
            # No re-raise, allow manager to exist without connection initially
            # raise  

    def _ensure_connection(self):
        """Asegura que la conexión a la base de datos esté activa."""
        if not self.conn or self.conn.closed != 0: # For psycopg2, conn.closed is non-zero if closed
            print("Conexión perdida o no establecida. Intentando reconectar...")
            self._connect()
        if not self.conn: # If _connect failed
             raise psycopg2.Error("No se pudo establecer la conexión a la base de datos.")


    def _create_table(self):
        """Crea la tabla de historial si no existe."""
        try:
            self._ensure_connection() # Ensure connection before creating table
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
            # No re-raise, if table creation fails, methods will handle it
            # raise

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
            self._ensure_connection()
            self.cursor.execute("INSERT INTO history (link, notes) VALUES (%s, %s)", (link, notes))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error al agregar enlace al historial en PostgreSQL: {e}")
            if self.conn and not self.conn.closed: # Check if conn exists and is not closed before rollback
                self.conn.rollback()
            return False
        # finally: # No longer closing connection here
            # pass 

    def get_history(self):
        """
        Obtiene el historial de enlaces.

        Returns:
            list: Una lista de tuplas, donde cada tupla contiene (link, notes, created_at).
                Retorna una lista vacía en caso de error.
        """
        try:
            self._ensure_connection()
            self.cursor.execute("SELECT link, notes, created_at FROM history ORDER BY created_at DESC")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al obtener el historial de PostgreSQL: {e}")
            return []
        # finally: # No longer closing connection here
            # pass

    def clear_history(self):
        """Elimina todo el historial."""
        try:
            self._ensure_connection()
            self.cursor.execute("DELETE FROM history")
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error al eliminar el historial en PostgreSQL: {e}")
            if self.conn and not self.conn.closed: # Check if conn exists and is not closed before rollback
                self.conn.rollback()
            return False
        # finally: # No longer closing connection here
            # pass

    def _close(self):
        """Cierra la conexión a la base de datos."""
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None


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