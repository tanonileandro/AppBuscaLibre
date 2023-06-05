import sqlite3
from datetime import datetime


class BuscaLibre:
    def __init__(self, conexion):
        self.conexion = conexion

    def cargar_libro(self, isbn, titulo, autor, genero, precio, cant_disponible):
        try:
            self.conexion.ejecutar_consulta("""
                INSERT INTO libros (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (isbn, titulo, autor, genero, precio, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cant_disponible))
            print("Libro cargado correctamente.")
        except sqlite3.Error as e:
            print(f"Error al cargar el libro: {e}")

    def modificar_precio_libro(self, id_libro, nuevo_precio):
        try:
            confirmacion = input("¿Está seguro que desea modificar el precio del libro? (S/N): ")
            if confirmacion.upper() == "S":
                self.conexion.ejecutar_consulta("""
                    UPDATE libros
                    SET precio = ?
                    WHERE id = ?
                """, (nuevo_precio, id_libro))
                print("Precio del libro modificado correctamente.")
        except sqlite3.Error as e:
            print(f"Error al modificar el precio del libro: {e}")

    def borrar_libro(self, id_libro):
        try:
            confirmacion = input("¿Está seguro que desea borrar el libro? (S/N): ")
            if confirmacion.upper() == "S":
                self.conexion.ejecutar_consulta("""
                    DELETE FROM libros
                    WHERE id = ?
                """, (id_libro,))
                print("Libro borrado correctamente.")
        except sqlite3.Error as e:
            print(f"Error al borrar el libro: {e}")

    def cargar_disponibilidad(self, id_libro, incremento_cant_disponible):
        try:
            self.conexion.ejecutar_consulta("""
                UPDATE libros
                SET cant_disponible = cant_disponible + ?
                WHERE id = ?
            """, (incremento_cant_disponible, id_libro))
            print("Disponibilidad cargada correctamente.")
        except sqlite3.Error as e:
            print(f"Error al cargar la disponibilidad: {e}")

    def listar_libros(self):
        try:
            registros = self.conexion.obtener_registros("""
                SELECT * FROM libros
                ORDER BY id, autor, titulo
            """)
            print("ID | ISBN | Título | Autor | Género | Precio | Fecha Último Precio | Cant. Disponible")
            for registro in registros:
                id_libro, isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible = registro
                print(
                    f"{id_libro} | {isbn} | {titulo} | {autor} | {genero} | {precio} | {fecha_ultimo_precio} | {cant_disponible}")
        except sqlite3.Error as e:
            print(f"Error al listar los libros: {e}")

    def registrar_venta(self, id_libro, cantidad):
        try:
            self.conexion.ejecutar_consulta("""
                INSERT INTO ventas (id_libro, cantidad, fecha)
                VALUES (?, ?, ?)
            """, (id_libro, cantidad, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.conexion.ejecutar_consulta("""
                UPDATE libros
                SET cant_disponible = cant_disponible - ?
                WHERE id = ?
            """, (cantidad, id_libro))
            print("Venta registrada correctamente.")
        except sqlite3.Error as e:
            print(f"Error al registrar la venta: {e}")

    def actualizar_precios(self, porcentaje_aumento):
        try:
            self.conexion.ejecutar_consulta("""
                INSERT INTO historico_libros
                SELECT * FROM libros
            """)
            self.conexion.ejecutar_consulta("""
                UPDATE libros
                SET precio = precio * (1 + ?)
            """, (porcentaje_aumento,))
            print("Precios actualizados correctamente.")
        except sqlite3.Error as e:
            print(f"Error al actualizar los precios: {e}")

    def mostrar_registros_anteriores_fecha(self, fecha):
        try:
            registros = self.conexion.obtener_registros("""
                SELECT * FROM libros
                WHERE fecha_ultimo_precio < ?
                ORDER BY id, autor, titulo
            """, (fecha,))
            print("ID | ISBN | Título | Autor | Género | Precio | Fecha Último Precio | Cant. Disponible")
            for registro in registros:
                id_libro, isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible = registro
                print(
                    f"{id_libro} | {isbn} | {titulo} | {autor} | {genero} | {precio} | {fecha_ultimo_precio} | {cant_disponible}")
        except sqlite3.Error as e:
            print(f"Error al mostrar los registros anteriores a la fecha: {e}")
