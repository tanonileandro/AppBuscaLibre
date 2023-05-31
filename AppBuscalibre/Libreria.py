from Conexion import Conexion
from logger_base import log


class Libreria:
    _SELECCIONAR = 'SELECT * FROM usuario ORDER BY id_usuario'
    _INSERTAR = 'INSERT INTO LIBROS (titulo, autor, precio, cantidadDisponibles) VALUES (?, ?, ?, ?)'
    _ACTUALIZAR = 'UPDATE usuario SET username=%s, password=%s WHERE id_usuario=%s'
    _ELIMINAR = 'DELETE FROM usuario WHERE id_usuario=%s'

    def __init__(self):
        self.conexion = Conexion()
        self.conexion.abrirConexion()
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS LIBROS")
        self.conexion.miCursor.execute("CREATE TABLE LIBROS (id_libro INTEGER PRIMARY KEY, titulo VARCHAR(30), "
                                       "autor VARCHAR(30), precio FLOAT "
                                       "NOT NULL, cantidadDisponibles INTEGER NOT NULL, UNIQUE(titulo, autor))")
        self.conexion.miConexion.commit()

    @classmethod
    def agregar_libro(cls, libro):
        try:
            valores = (libro.titulo, libro.autor, libro.precio, libro.cantidadDisponibles)
            cls.conexion.miCursor.execute(cls._INSERTAR, valores)
            cls.conexion.miConexion.commit()
            log.debug(f'Libro agregado: {libro}')
        except Exception as e:
            print(f'Error al agregar un libro: {e}')
