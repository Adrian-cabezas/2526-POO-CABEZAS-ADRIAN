"""
Programa para convertir unidades de medida.
Convierte metros a kilómetros utilizando datos ingresados por el usuario.
"""

# ----------  Conversión de Metros a Kilómetros  ----------

# Solicitar el nombre del usuario (string)
user_name = input("Ingrese su nombre: ")

# Solicitar la cantidad en metros (float)
meters = float(input("Ingrese la cantidad en metros: "))

# Conversión de metros a kilómetros (float)
kilometers = meters / 1000

# Verificar si la distancia es mayor o igual a 1 km (boolean)
is_long_distance = kilometers >= 1

# ----------  Resultados de la Conversión  ----------

print("\nResultados de la conversión:")
print("------------------------------")
print("Usuario:", user_name)
print("Metros ingresados:", meters)
print("Kilómetros equivalentes:", kilometers)
print("------------------------------")

# Evaluar la distancia convertida
if is_long_distance:
    print("La distancia es larga (1 km o más).")
else:
    print("La distancia es corta (menos de 1 km).")
print("------------------------------")
