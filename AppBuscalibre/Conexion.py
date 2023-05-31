import sqlite3


class Conexion:
    def __init__(self):
        self.miCursor = None
        self.miConexion = None

    def abrirConexion(self):
        self.miConexion = sqlite3.connect("Libreria.db")
        self.miCursor = self.miConexion.cursor()

    def cerrarConexion(self):
        self.miConexion.close()
