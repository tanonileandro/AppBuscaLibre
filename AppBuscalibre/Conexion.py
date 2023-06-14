import sqlite3
from logger_base import log


class ConexionSQLite:
    def __init__(self, archivo_db):
        self.archivo_db = archivo_db
        self.conexion = None
        self.cursor = None

# Establecer conexión con la base de datos
    def conectar(self):
        try:
            self.conexion = sqlite3.connect(self.archivo_db)
            self.cursor = self.conexion.cursor()
            print("> Conexión exitosa a la base de datos <")
        except sqlite3.Error as e:
            log.error(f"Error al conectar a la base de datos: {e}")

# Cerrar la conexión y liberar recursos de la base de datos 
    def desconectar(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conexion:
                self.conexion.close()
            print(" > Desconexión exitosa de la base de datos <")
        except sqlite3.Error as e:
            log.error(f"Error al desconectar de la base de datos: {e}")

# Ejecutar consulta y obtener registro
    def obtener_registro(self, consulta):
        try:
            self.cursor.execute(consulta)
            registro = self.cursor.fetchone()
            return registro
        except Exception as e:
            log.error("Error al obtener el registro:", e)

# Ejecutar consulta con o sin parámetros
    def ejecutar_consulta(self, consulta, parametros=None):
        try:
            if parametros:
                self.cursor.execute(consulta, parametros)
            else:
                self.cursor.execute(consulta)
            self.conexion.commit()
        except sqlite3.Error as e:
            log.error(f"Error al ejecutar la consulta: {e}")

# Devolver todos los registros resultantes 
    def obtener_registros(self, consulta, parametros=None):
        try:
            if parametros:
                self.cursor.execute(consulta, parametros)
            else:
                self.cursor.execute(consulta)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            log.error(f"Error al obtener los registros: {e}")
            return []

# Crear una tabla y registrar cualquier error
    def crear_tabla(self, consulta):
        try:
            self.cursor.execute(consulta)
            self.conexion.commit()
        except sqlite3.Error as e:
            log.error(f"Error al crear la tabla: {e}")
