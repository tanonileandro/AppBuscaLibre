import sqlite3


class Conexiones:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.conexion = None
        self.miCursor = None

    def conectar(self):
        try:
            self.conexion = sqlite3.connect(self.nombre_archivo)
            self.miCursor = self.conexion.cursor()
            self.crear_tabla_libros()
            self.crear_tabla_ventas()
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def desconectar(self):
        if self.conexion:
            self.conexion.close()
            self.conexion = None
            print("Desconexión exitosa.")

    def ejecutar_consulta(self, consulta, parametros=None):
        try:
            if self.miCursor:
                if parametros:
                    self.miCursor.execute(consulta, parametros)
                else:
                    self.miCursor.execute(consulta)
                self.conexion.commit()
            else:
                print("Error: El cursor no está disponible.")
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")

    def obtener_registros(self, consulta, parametros=None):
        try:
            if self.miCursor:
                if parametros:
                    self.miCursor.execute(consulta, parametros)
                else:
                    self.miCursor.execute(consulta)
                return self.miCursor.fetchall()
            else:
                print("Error: El cursor no está disponible.")
        except sqlite3.Error as e:
            print(f"Error al obtener los registros: {e}")

    def crear_tabla_libros(self):
        try:
            self.miCursor.execute("""
                CREATE TABLE IF NOT EXISTS libros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn TEXT UNIQUE,
                    titulo TEXT,
                    autor TEXT,
                    genero TEXT,
                    precio REAL,
                    fecha_ultimo_precio TEXT,
                    cant_disponible INTEGER
                )
            """)
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla libros: {e}")

    def crear_tabla_ventas(self):
        try:
            self.miCursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_libro INTEGER,
                    cantidad INTEGER,
                    fecha TEXT,
                    FOREIGN KEY (id_libro) REFERENCES libros (id)
                )
            """)
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla ventas: {e}")
