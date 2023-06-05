from conexion import Conexiones
from buscaLibre import BuscaLibre


class Menu:
    def __init__(self, biblioteca):
        self.biblioteca = biblioteca

    def mostrar_menu(self):
        print("MENÚ BUSCALIBRE")
        print("1- Cargar Libros")
        print("2- Modificar precio de un libro")
        print("3- Borrar un libro")
        print("4- Cargar disponibilidad")
        print("5- Listado de Libros")
        print("6- Ventas")
        print("7- Actualizar Precios")
        print("8- Mostrar registros anteriores a una fecha")
        print("0- Salir")

    def ejecutar_opcion(self, opcion):
        try:
            if opcion == 1:
                isbn = input("Ingrese el ISBN: ")
                titulo = input("Ingrese el título: ")
                autor = input("Ingrese el autor: ")
                genero = input("Ingrese el género: ")
                precio = float(input("Ingrese el precio: "))
                cant_disponible = int(input("Ingrese la cantidad disponible: "))
                self.biblioteca.cargar_libro(isbn, titulo, autor, genero, precio, cant_disponible)
            elif opcion == 2:
                id_libro = int(input("Ingrese el ID del libro: "))
                nuevo_precio = float(input("Ingrese el nuevo precio: "))
                self.biblioteca.modificar_precio_libro(id_libro, nuevo_precio)
            elif opcion == 3:
                id_libro = int(input("Ingrese el ID del libro: "))
                self.biblioteca.borrar_libro(id_libro)
            elif opcion == 4:
                id_libro = int(input("Ingrese el ID del libro: "))
                incremento_cant_disponible = int(input("Ingrese la cantidad a incrementar: "))
                self.biblioteca.cargar_disponibilidad(id_libro, incremento_cant_disponible)
            elif opcion == 5:
                self.biblioteca.listar_libros()
            elif opcion == 6:
                id_libro = int(input("Ingrese el ID del libro vendido: "))
                cantidad = int(input("Ingrese la cantidad vendida: "))
                self.biblioteca.registrar_venta(id_libro, cantidad)
            elif opcion == 7:
                porcentaje_aumento = float(input("Ingrese el porcentaje de aumento de precios: "))
                self.biblioteca.actualizar_precios(porcentaje_aumento)
            elif opcion == 8:
                fecha = input("Ingrese la fecha (AAAA-MM-DD HH:MM:SS): ")
                self.biblioteca.mostrar_registros_anteriores_fecha(fecha)
            elif opcion == 0:
                print("Saliendo del programa...")
            else:
                print("Opción inválida. Por favor, ingrese una opción válida.")

        except ValueError:
            print("Error: entrada inválida. Asegúrese de ingresar valores numéricos correctamente.")

        except Exception as e:
            print(f"Error inesperado: {str(e)}")


def main():
    nombre_archivo = "C:/SourceCode/UTN/ProgramacionII/utn-programacionII-integrador/AppBuscalibre/buscaLibre.db"
    conexion = Conexiones(nombre_archivo)
    conexion.conectar()

    biblioteca = BuscaLibre(conexion)

    menu = Menu(biblioteca)

    opcion = None
    while opcion != 0:
        menu.mostrar_menu()
        opcion = int(input("Ingrese una opción: "))
        menu.ejecutar_opcion(opcion)

    conexion.desconectar()


if __name__ == '__main__':
    main()
