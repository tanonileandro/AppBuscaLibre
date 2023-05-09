"""Conversiones Básicas"""

"""
Convertir los numeros de string a enteros y luego sumarlos.
"""

numero_01 = "123"
numero_02 = "456"
numero_03 = "789"
numero_04 = "132"

# COMPLETAR - INICIO
numero_int1 = int(numero_01)
numero_int2 = int(numero_02)
numero_int3 = int(numero_03)
numero_int4 = int(numero_04)

suma_de_numeros = numero_int1 + numero_int2 + numero_int3 + numero_int4
# COMPLETAR - FIN
print(f'La suma de todos los números convertidos es: {suma_de_numeros}')

assert suma_de_numeros == 1500

"""
Convertir los numeros de enteros a string y luego concatenarlos.
"""

numero_01 = 123
numero_02 = 456
numero_03 = 789

# COMPLETAR - INICIO
numero_str1 = str(numero_01)
numero_str2 = str(numero_02)
numero_str3 = str(numero_03)

suma_de_numeros_string = numero_str1 + numero_str2 + numero_str3
# COMPLETAR - FIN
print(f'La suma de todos los números convertidos y concatenados es: {suma_de_numeros_string}')

assert suma_de_numeros_string == "123456789"

"""
Convertir los numeros de binario, octal y hexadecimal a enteros y luego
multiplicarlos.
"""

numero_binario = "0b111010110101110111101000000"
numero_octal = "0o1425"
numero_hexadecimal = "0x6f540"

# COMPLETAR - INICIO
num_entero_binario = int(numero_binario, 2)
num_entero_octal = int(numero_octal, 8)
num_entero_hexadecimal = int(numero_hexadecimal, 16)

multiplicacion_de_numeros = num_entero_binario * num_entero_octal * num_entero_hexadecimal
# COMPLETAR - FIN
print(f'El resultado de la multiplicación es: {multiplicacion_de_numeros}')

assert multiplicacion_de_numeros == 44397345600000000

"""
Convertir todo los numeros a enteros y luego restarlos secuencialmente (El uno
menos el dos menos el tres menos el cuatro).
"""

numero_01 = "987"
numero_02 = "0x6f54F"
numero_03 = "0o1234"
numero_04 = 654

# COMPLETAR - INICIO
num_entero1 = int(numero_01)
num_entero2 = int(numero_02, 16)
num_entero3 = int(numero_03, 0)

resultado_resta = num_entero1 - num_entero2 - num_entero3 - numero_04
# COMPLETAR - FIN
print(f'El resultado de la resta es: {resultado_resta}')

assert resultado_resta == -456350
