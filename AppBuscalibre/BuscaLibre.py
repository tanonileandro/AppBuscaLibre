from datetime import datetime
import logging as log


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
        except Exception as e:
            log.error(f"Error al crear la tabla de libros: {e}")

    def crear_tabla_ventas(self):
        consulta = """
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_libro INTEGER,
                cantidad INTEGER,
                fecha TEXT,
                precio REAL,
                FOREIGN KEY (id_libro) REFERENCES libros (id)
            )
            """
        try:
            self.conexion.crear_tabla(consulta)
        except Exception as e:
            log.error(f"Error al crear la tabla de ventas: {e}")

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
            log.error(f"Error al crear la tabla de historico_libros: {e}")

    def cargar_libros(self):
        try:
            print(" Cargar Libro ".center(60, '-'))

            # Verificar si se desea salir
            opcion_salir = input("\nPresione cualquier valor para continuar o \"0\" para volver al menú: ")
            if opcion_salir == "0":
                return

            isbn = input("ISBN: ")
            titulo = input("Título: ")
            autor = input("Autor: ")
            genero = input("Género: ")
            precio = float(input("Precio: $"))
            fecha_ultimo_precio = datetime.today().strftime("%Y-%m-%d")
            cant_disponible = int(input("Cant. Disponible: "))

            consulta = "INSERT INTO libros (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, " \
                       "cant_disponible) VALUES (?, ?, ?, ?, ?, ?, ?)"
            parametros = (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible)

            self.conexion.ejecutar_consulta(consulta, parametros)

            print("\nLibro cargado correctamente.")
        except Exception as e:
            log.error(f"\nError al cargar el libro: {e}")

    def modificar_precio_libro(self):
        try:
            print(" Modificar precio de un Libro ".center(60, '-'))

            # Verificar si se desea salir
            opcion_salir = input("\nPresione cualquier valor para continuar o \"0\" para volver al menú: ")
            if opcion_salir == "0":
                return

            id_libro = int(input("Ingrese el ID: "))

            # Verificar si el libro existe
            consulta_verificar = f"SELECT COUNT(*) FROM libros WHERE id={id_libro}"
            resultado_verificar = self.conexion.obtener_registro(consulta_verificar)

            if resultado_verificar[0] > 0:
                # Obtener información del libro
                consulta = f"SELECT * FROM libros WHERE id={id_libro}"
                libro = self.conexion.obtener_registro(consulta)

                # Mostrar información del libro
                print("\n> Información del libro: ")
                print(f"ID: {libro[0]}, ISBN: {libro[1]}, Título: {libro[2]}, Autor: {libro[3]}, "
                      f"Género: {libro[4]}, Precio: ${libro[5]:.2f}, Fecha Último Precio: {libro[6]}, "
                      f"CantDisponible: {libro[7]}")

                # Confirmar modificación del precio
                confirmacion = input("\n¿Desea modificar el precio del libro? (s/n): ")

                if confirmacion.lower() == "s":
                    # Actualizar precio del libro
                    nuevo_precio = float(input("\nIngrese el nuevo precio: "))
                    consulta = f"UPDATE libros SET precio={nuevo_precio}, fecha_ultimo_precio=DATETIME('now') " \
                               f"WHERE id={id_libro}"
                    self.conexion.ejecutar_consulta(consulta)

                    print("\nPrecio del libro modificado correctamente.")
                else:
                    print("\nNo se realizó la modificación del precio del libro.")
            else:
                print("\nNo se encontró un libro con el ID especificado.")
        except ValueError:
            print("\nError: Ingrese un valor numérico válido para el ID del libro.")
        except Exception as e:
            log.error(f"\nError al modificar el precio del libro: {e}")

    def borrar_libro(self):
        try:
            print(" Borrar Libro ".center(60, '-'))

            # Verificar si se desea salir
            opcion_salir = input("\nPresione cualquier valor para continuar o \"0\" para volver al menú: ")
            if opcion_salir == "0":
                return

            id_libro = int(input("ID del libro: "))

            # Verificar si el libro existe
            consulta_verificar = f"SELECT COUNT(*) FROM libros WHERE id={id_libro}"
            resultado_verificar = self.conexion.obtener_registro(consulta_verificar)

            if resultado_verificar[0] > 0:
                consulta_select = "SELECT * FROM libros WHERE id = ?"
                parametros_select = (id_libro,)
                registro = self.conexion.obtener_registros(consulta_select, parametros_select)

                print("\n> Información del libro: ")
                if registro:
                    libro = registro[0]
                    isbn = libro[1]
                    titulo = libro[2]
                    autor = libro[3]
                    genero = libro[4]
                    precio = libro[5]
                    fecha_ultimo_precio = libro[6]
                    cant_disponible = libro[7]

                    print(f"ID: {libro[0]} | ISBN: {libro[1]} | Título: {libro[2]} | Autor: {libro[3]} | "
                          f"Género: {libro[4]} \n")

                    confirmacion = input("¿Desea borrar este libro? (s/n): ")

                    if confirmacion.lower() == "s":
                        consulta_insert = "INSERT INTO historico_libros (isbn, titulo, autor, genero, precio, " \
                                          "fecha_ultimo_precio, " \
                                          "cant_disponible) VALUES (?, ?, ?, ?, ?, ?, ?)"
                        parametros_insert = (
                            isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible)

                        consulta_delete = "DELETE FROM libros WHERE id = ?"
                        parametros_delete = (id_libro,)

                        self.conexion.ejecutar_consulta(consulta_insert, parametros_insert)
                        self.conexion.ejecutar_consulta(consulta_delete, parametros_delete)

                        print("\nLibro borrado correctamente.")
                    else:
                        print("\nNo se realizó el borrado del libro.")
            else:
                print("\nEl ID del libro no existe.")
        except Exception as e:
            log.error(f"\nError al borrar el libro {e}")

    def cargar_disponibilidad(self):
        try:
            print(" Cargar Disponibilidad ".center(60, '-'))
            print("-> La cantidad que agregue se sumará al stock actual <-".center(60, ' '))

            # Verificar si se desea salir
            opcion_salir = input("\nPresione cualquier valor para continuar o \"0\" para volver al menú: ")
            if opcion_salir == "0":
                return

            id_libro = int(input("ID del libro: "))

            # Verificar si el libro existe
            consulta_verificar = f"SELECT COUNT(*) FROM libros WHERE id={id_libro}"
            resultado_verificar = self.conexion.obtener_registro(consulta_verificar)

            if resultado_verificar[0] > 0:
                consulta_select = "SELECT * FROM libros WHERE id = ?"
                parametros_select = (id_libro,)
                registro = self.conexion.obtener_registros(consulta_select, parametros_select)

                if registro:
                    libro = registro[0]
                    cant_disponible_actual = libro[7]

                    print("\n> Información del libro: ")
                    print(f"ID: {libro[0]} | ISBN: {libro[1]} | Título: {libro[2]} | Autor: {libro[3]}"
                          f" | CantDisponible: {libro[7]} \n")

                    incremento = int(input("Cantidad a incrementar: "))

                    confirmacion = input("¿Desea cargar la disponibilidad? (s/n): ")

                    if confirmacion.lower() == "s":
                        cant_disponible_nueva = cant_disponible_actual + incremento

                        consulta_update = "UPDATE libros SET cant_disponible = ? WHERE id = ?"
                        parametros_update = (cant_disponible_nueva, id_libro)

                        self.conexion.ejecutar_consulta(consulta_update, parametros_update)

                        print("\nDisponibilidad cargada correctamente.")
                    else:
                        print("\nNo se realizó la carga de disponibilidad.")
            else:
                print("\nEl ID del libro no existe.")
        except Exception as e:
            log.error(f"\nError al cargar la disponibilidad: {e}")

    def listar_libros(self):
        consulta = "SELECT * FROM libros ORDER BY id, autor, titulo"
        registros = self.conexion.obtener_registros(consulta)

        if registros:
            print("> Listado de Libros:")
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
                      f"Precio: ${precio:.2f} | Fecha ultimo precio: {fecha_ultimo_precio} | "
                      f"Cant. disponible: {cant_disponible}")
        else:
            print("\nNo hay libros para mostrar.")

    def realizar_venta(self):
        try:
            print(" Registrar Venta ".center(60, '-'))
            # Verificar si se desea salir
            opcion_salir = input("\nPresione cualquier valor para continuar o \"0\" para volver al menú: ")
            if opcion_salir == "0":
                return

            id_libro = int(input("ID del libro vendido: "))

            consulta_select = "SELECT * FROM libros WHERE id = ?"
            parametros_select = (id_libro,)
            registro_libro = self.conexion.obtener_registros(consulta_select, parametros_select)

            if registro_libro:
                libro = registro_libro[0]
                cant_disponible_actual = libro[7]
                precio_venta = libro[5]

                print("\n> Información del libro: ")
                print(f"ID: {libro[0]} | ISBN: {libro[1]} | Título: {libro[2]} | Autor: {libro[3]} | "
                      f"Género: {libro[4]} | Precio: ${libro[5]:.2f} | Fecha Último Precio: {libro[6]} | "
                      f"Cant. Disponible: {libro[7]}")

                cantidad = int(input("\nCantidad vendida: "))

                if cantidad <= cant_disponible_actual:
                    consulta_insert_venta = "INSERT INTO ventas (id_libro, cantidad, fecha, precio) VALUES (?, ?, ?, ?)"
                    parametros_insert_venta = (id_libro, cantidad, datetime.today().strftime("%Y-%m-%d"), precio_venta)

                    consulta_update_libro = "UPDATE libros SET cant_disponible = ? WHERE id = ?"
                    parametros_update_libro = (cant_disponible_actual - cantidad, id_libro)

                    self.conexion.ejecutar_consulta(consulta_insert_venta, parametros_insert_venta)
                    self.conexion.ejecutar_consulta(consulta_update_libro, parametros_update_libro)

                    print("\nVenta realizada correctamente.")
                else:
                    print("\nNo hay suficiente disponibilidad del libro.")
            else:
                print("\nEl ID del libro no existe.")
        except Exception as e:
            log.error(f"Error al realizar la venta: {e}")

    def actualizar_precios(self):
        try:
            print(" Actualizar Precios ".center(60, '-'))

            # Verificar si se desea salir
            opcion_salir = input("\nPresione cualquier valor para continuar o \"0\" para volver al menú: ")
            if opcion_salir == "0":
                return

            porcentaje_aumento = float(input("\nIngrese el porcentaje de aumento de precios (%): "))

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
                    parametros_update_libro = (nuevo_precio, datetime.today().strftime("%Y-%m-%d"), id_libro)

                    self.conexion.ejecutar_consulta(consulta_insert_historico, parametros_insert_historico)
                    self.conexion.ejecutar_consulta(consulta_update_libro, parametros_update_libro)

                print("\nPrecios actualizados correctamente.")
            else:
                print("\nNo hay libros para actualizar los precios.")
        except Exception as e:
            log.error(f"\nError al actualizar los precios: {e}")

    def mostrar_registros_anteriores_fecha(self):
        try:
            print(" Registros Anteriores ".center(60, '-'))

            fecha_valida = False
            while not fecha_valida:
                fecha_limite = input("Ingrese la fecha límite (YYYY-MM-DD): ")
                try:
                    datetime.strptime(fecha_limite, "%Y-%m-%d")
                    fecha_valida = True
                except ValueError:
                    print("\nFormato de fecha inválido. Por favor, ingrese la fecha en el formato YYYY-MM-DD.")

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

                    print("\n> Información del libro: ")
                    print(f"ID: {id_libro} | ISBN: {isbn} | Título: {titulo} | Autor: {autor} | Género: {genero} | "
                          f"Precio: ${precio:.2f} | Fecha último precio: {fecha_ultimo_precio} | "
                          f"Cant. disponible: {cant_disponible}")
            else:
                print("\nNo hay registros anteriores a la fecha límite.")
        except Exception as e:
            log.error(f"\nError al mostrar los registros anteriores a la fecha: {e}")

    def mostrar_historico_libros(self):
        try:
            print(" Historial de Precios ".center(60, '-'))

            consulta = "SELECT * FROM historico_libros"
            registros = self.conexion.obtener_registros(consulta)

            if registros:
                print("\n> Información del libro: ")
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
                          f"Precio: ${precio:.2f} | Fecha ultimo precio: {fecha_ultimo_precio} | "
                          f"Cant. disponible: {cant_disponible}")
            else:
                print("No hay registros en el historial de libros.")
        except Exception as e:
            log.error(f"Error al mostrar el historial de libros: {e}")

    def mostrar_ventas(self):
        try:
            print(" Historial de Ventas ".center(60, '-'))

            consulta = "SELECT * FROM ventas"
            registros = self.conexion.obtener_registros(consulta)

            if registros:
                print("\n> Información del libro: ")
                for registro in registros:
                    id_venta = registro[0]
                    id_libro = registro[1]
                    cantidad = registro[2]
                    fecha = registro[3]
                    precio = registro[4]

                    print(f"ID Venta: {id_venta} | ID Libro: {id_libro} | Cantidad: {cantidad} | Fecha: {fecha} | "
                          f"Precio/Unidad: {precio:.2f}")
            else:
                print("No hay registros de ventas.")
        except Exception as e:
            log.error(f"Error al mostrar las ventas: {e}")
