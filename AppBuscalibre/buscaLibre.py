from datetime import date
import datetime


class BuscaLibre:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear_tabla_libros(self):
        consulta = """
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
        """
        try:
            self.conexion.crear_tabla(consulta)
        except:
            print("Error al crear la tabla de libros.")

    def crear_tabla_ventas(self):
        consulta = """
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_libro INTEGER,
                cantidad INTEGER,
                fecha TEXT,
                FOREIGN KEY (id_libro) REFERENCES libros (id)
            )
        """
        try:
            self.conexion.crear_tabla(consulta)
        except Exception as e:
            print(f"Error al crear la tabla de ventas: {e}")

    def crear_tabla_historico_libros(self):
        consulta = """
            CREATE TABLE IF NOT EXISTS historico_libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT,
                titulo TEXT,
                autor TEXT,
                genero TEXT,
                precio REAL,
                fecha_ultimo_precio TEXT,
                cant_disponible INTEGER
            )
        """
        try:
            self.conexion.crear_tabla(consulta)
        except Exception as e:
            print(f"Error al crear la tabla de historico_libros: {e}")

    def cargar_libros(self):
        try:
            isbn = input("ISBN: ")
            titulo = input("Título: ")
            autor = input("Autor: ")
            genero = input("Género: ")
            precio = float(input("Precio: $"))
            fecha_ultimo_precio = date.today().strftime("%Y-%m-%d")
            cant_disponible = int(input("CantDisponible: "))

            consulta = "INSERT INTO libros (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible) " \
                       "VALUES (?, ?, ?, ?, ?, ?, ?)"
            parametros = (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible)

            self.conexion.ejecutar_consulta(consulta, parametros)

            print("Libro cargado correctamente.")
        except Exception as e:
            print(f"Error al cargar el libro: {e}")

    def modificar_precio_libro(self):
        try:
            id_libro = int(input("Ingrese el ID del libro: "))
            nuevo_precio = float(input("Ingrese el nuevo precio: "))

            # Obtener información del libro
            consulta = f"SELECT * FROM libros WHERE id={id_libro}"
            libro = self.conexion.obtener_registro(consulta)

            if libro:
                # Mostrar información del libro
                print("\nInformación del libro:")
                print(f"ID: {libro[0]}, ISBN: {libro[1]}, Título: {libro[2]}, Autor: {libro[3]}, "
                      f"Género: {libro[4]}, Precio: {libro[5]:.2f}, Fecha Último Precio: {libro[6]}, "
                      f"CantDisponible: {libro[7]}")

                # Confirmar modificación del precio
                confirmacion = input("¿Desea modificar el precio del libro? (s/n): ")

                if confirmacion.lower() == "s":
                    # Actualizar precio del libro
                    consulta = f"UPDATE libros SET precio={nuevo_precio}, fecha_ultimo_precio=DATETIME('now') " \
                               f"WHERE id={id_libro}"
                    self.conexion.ejecutar_consulta(consulta)

                    print("Precio del libro modificado correctamente.")
                else:
                    print("No se realizó la modificación del precio del libro.")
            else:
                print("No se encontró un libro con el ID especificado.")
        except ValueError:
            print("Error: Ingrese un valor numérico válido para el ID del libro.")
        except Exception as e:
            print(f"Error al modificar el precio del libro: {e}")

    def borrar_libro(self):
        try:
            id_libro = int(input("ID del libro: "))

            consulta_select = "SELECT * FROM libros WHERE id = ?"
            parametros_select = (id_libro,)
            registro = self.conexion.obtener_registros(consulta_select, parametros_select)

            if registro:
                libro = registro[0]
                isbn = libro[1]
                titulo = libro[2]
                autor = libro[3]
                genero = libro[4]
                precio = libro[5]
                fecha_ultimo_precio = libro[6]
                cant_disponible = libro[7]

                consulta_insert = "INSERT INTO historico_libros (isbn, titulo, autor, genero, precio, " \
                                  "fecha_ultimo_precio, " \
                                  "cant_disponible) VALUES (?, ?, ?, ?, ?, ?, ?)"
                parametros_insert = (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible)

                consulta_delete = "DELETE FROM libros WHERE id = ?"
                parametros_delete = (id_libro,)

                self.conexion.ejecutar_consulta(consulta_insert, parametros_insert)
                self.conexion.ejecutar_consulta(consulta_delete, parametros_delete)

                print("Libro borrado correctamente.")
            else:
                print("El ID del libro no existe.")
        except Exception as e:
            print(f"Error al borrar el libro {e}")

    def cargar_disponibilidad(self):
        try:
            id_libro = int(input("ID del libro: "))
            incremento = int(input("Cantidad a incrementar: "))

            consulta_select = "SELECT * FROM libros WHERE id = ?"
            parametros_select = (id_libro,)
            registro = self.conexion.obtener_registros(consulta_select, parametros_select)

            if registro:
                cant_disponible_actual = registro[0][7]
                cant_disponible_nueva = cant_disponible_actual + incremento

                consulta_update = "UPDATE libros SET cant_disponible = ? WHERE id = ?"
                parametros_update = (cant_disponible_nueva, id_libro)

                self.conexion.ejecutar_consulta(consulta_update, parametros_update)

                print("Disponibilidad cargada correctamente.")
            else:
                print("El ID del libro no existe.")
        except Exception as e:
            print(f"Error al cargar la disponibilidad: {e}")

    def listar_libros(self):
        consulta = "SELECT * FROM libros ORDER BY id, autor, titulo"
        registros = self.conexion.obtener_registros(consulta)

        if registros:
            print("\nListado de Libros:")
            for registro in registros:
                id_libro = registro[0]
                isbn = registro[1]
                titulo = registro[2]
                autor = registro[3]
                genero = registro[4]
                precio = registro[5]
                fecha_ultimo_precio = registro[6]
                cant_disponible = registro[7]

                print(f"ID: {id_libro} | ISBN: {isbn} | Título: {titulo} | Autor: {autor} | Genero: {genero} | "
                      f"Precio: {precio:.2f} | Fecha ultimo precio: {fecha_ultimo_precio} | "
                      f"Cant. disponible: {cant_disponible}")
        else:
            print("No hay libros para mostrar.")

    def realizar_venta(self):
        try:
            id_libro = int(input("ID del libro vendido: "))
            cantidad = int(input("Cantidad vendida: "))

            consulta_select = "SELECT * FROM libros WHERE id = ?"
            parametros_select = (id_libro,)
            registro_libro = self.conexion.obtener_registros(consulta_select, parametros_select)

            if registro_libro:
                libro = registro_libro[0]
                cant_disponible_actual = libro[7]

                if cantidad <= cant_disponible_actual:
                    consulta_insert_venta = "INSERT INTO ventas (id_libro, cantidad, fecha) VALUES (?, ?, ?)"
                    parametros_insert_venta = (id_libro, cantidad, date.today().strftime("%Y-%m-%d"))

                    consulta_update_libro = "UPDATE libros SET cant_disponible = ? WHERE id = ?"
                    parametros_update_libro = (cant_disponible_actual - cantidad, id_libro)

                    self.conexion.ejecutar_consulta(consulta_insert_venta, parametros_insert_venta)
                    self.conexion.ejecutar_consulta(consulta_update_libro, parametros_update_libro)

                    print("Venta realizada correctamente.")
                else:
                    print("No hay suficiente disponibilidad del libro.")
            else:
                print("El ID del libro no existe.")
        except Exception as e:
            print(f"Error al realizar la venta: {e}")

    def actualizar_precios(self):
        try:
            porcentaje_aumento = float(input("Porcentaje de aumento de precios: "))

            consulta_select_libros = "SELECT * FROM libros"
            registros_libros = self.conexion.obtener_registros(consulta_select_libros)

            if registros_libros:
                for libro in registros_libros:
                    id_libro = libro[0]
                    isbn = libro[1]
                    titulo = libro[2]
                    autor = libro[3]
                    genero = libro[4]
                    precio_actual = libro[5]
                    fecha_ultimo_precio = libro[6]
                    cant_disponible = libro[7]

                    nuevo_precio = precio_actual + (precio_actual * porcentaje_aumento / 100)

                    consulta_insert_historico = "INSERT INTO historico_libros (isbn, titulo, autor, genero, precio, " \
                                                "fecha_ultimo_precio, cant_disponible) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    parametros_insert_historico = (
                        isbn, titulo, autor, genero, precio_actual, fecha_ultimo_precio, cant_disponible)

                    consulta_update_libro = "UPDATE libros SET precio = ?, fecha_ultimo_precio = ? WHERE id = ?"
                    parametros_update_libro = (nuevo_precio, date.today().strftime("%Y-%m-%d"), id_libro)

                    self.conexion.ejecutar_consulta(consulta_insert_historico, parametros_insert_historico)
                    self.conexion.ejecutar_consulta(consulta_update_libro, parametros_update_libro)

                print("Precios actualizados correctamente.")
            else:
                print("No hay libros para actualizar los precios.")
        except Exception as e:
            print(f"Error al actualizar los precios: {e}")


    def mostrar_registros_anteriores_fecha(self):
        try:
            fecha_valida = False
            while not fecha_valida:
                fecha_limite = input("Ingrese la fecha límite (YYYY-MM-DD): ")
                try:
                    datetime.datetime.strptime(fecha_limite, "%Y-%m-%d")
                    fecha_valida = True
                except ValueError:
                    print("Formato de fecha inválido. Por favor, ingrese la fecha en el formato YYYY-MM-DD.")

            consulta = "SELECT * FROM libros WHERE fecha_ultimo_precio <= ?"
            parametros = (fecha_limite,)
            registros = self.conexion.obtener_registros(consulta, parametros)

            if registros:
                print("\nRegistros anteriores a la fecha límite:")
                for registro in registros:
                    id_libro = registro[0]
                    isbn = registro[1]
                    titulo = registro[2]
                    autor = registro[3]
                    genero = registro[4]
                    precio = registro[5]
                    fecha_ultimo_precio = registro[6]
                    cant_disponible = registro[7]

                    print(f"ID: {id_libro} | ISBN: {isbn} | Título: {titulo} | Autor: {autor} | Género: {genero} | "
                          f"Precio: {precio:.2f} | Fecha último precio: {fecha_ultimo_precio} | "
                          f"Cant. disponible: {cant_disponible}")
            else:
                print("No hay registros anteriores a la fecha límite.")
        except Exception as e:
            print(f"Error al mostrar los registros anteriores a la fecha: {e}")

    def mostrar_historico_libros(self):
        try:
            consulta = "SELECT * FROM historico_libros"
            registros = self.conexion.obtener_registros(consulta)

            if registros:
                print("Historial de Libros:")
                for registro in registros:
                    id_libro = registro[0]
                    isbn = registro[1]
                    titulo = registro[2]
                    autor = registro[3]
                    genero = registro[4]
                    precio = registro[5]
                    fecha_ultimo_precio = registro[6]
                    cant_disponible = registro[7]

                    print(f"ID: {id_libro} | ISBN: {isbn} | Título: {titulo} | Autor: {autor} | Genero: {genero} | "
                          f"Precio: {precio:.2f} | Fecha ultimo precio: {fecha_ultimo_precio} | "
                          f"Cant. disponible: {cant_disponible}")
            else:
                print("No hay registros en el historial de libros.")
        except Exception as e:
            print(f"Error al mostrar el historial de libros: {e}")

    def mostrar_ventas(self):
        try:
            consulta = "SELECT * FROM ventas"
            registros = self.conexion.obtener_registros(consulta)

            if registros:
                print("Registro de Ventas:")
                for registro in registros:
                    id_venta = registro[0]
                    id_libro = registro[1]
                    cantidad = registro[2]
                    fecha = registro[3]

                    print(f"ID Venta: {id_venta}, ID Libro: {id_libro}, Cantidad: {cantidad}, Fecha: {fecha}")
            else:
                print("No hay registros de ventas.")
        except Exception as e:
            print(f"Error al mostrar las ventas: {e}")
