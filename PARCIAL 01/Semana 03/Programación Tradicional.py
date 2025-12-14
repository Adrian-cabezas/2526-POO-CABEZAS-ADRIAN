"""
Calcular el promedio de temperaturas por ciudad.

Se presenta una matriz donde cada fila representa una ciudad y cada columna
es una medición diaria. El programa recorre cada fila, suma las temperaturas
y calcula el promedio semanal por ciudad.

Requisitos cumplidos:
1. Uso de programación tradicional basada en funciones.
2. Funciones separadas para:
   - Entrada de datos diarios (temperaturas).
   - Cálculo del promedio semanal.
3. Organización lógica y funcional del código.
"""

from typing import List

# --------------------------------------------------
# Función 1: Entrada de datos diarios
# --------------------------------------------------
def ingresar_temperaturas(ciudades: List[str], dias_por_semana: int = 7) -> List[List[float]]:
    """
    Solicita por teclado las temperaturas diarias de cada ciudad.

    Parámetros:
        ciudades: lista de nombres de ciudades.
        dias_por_semana: número de días a registrar (por defecto 7).

    Retorna:
        Matriz de temperaturas (lista de listas).
    """
    temperaturas: List[List[float]] = []

    for ciudad in ciudades:
        print(f"\nIngreso de temperaturas para {ciudad}:")
        semana: List[float] = []

        for dia in range(1, dias_por_semana + 1):
            while True:
                try:
                    temp = float(input(f"  Día {dia}: "))
                    semana.append(temp)
                    break
                except ValueError:
                    print("  Error: ingrese un número válido.")

        temperaturas.append(semana)

    return temperaturas
# Función 2: Cálculo del promedio semanal
def calcular_promedio_semanal(temperaturas_ciudad: List[float]) -> float:
    """
    Calcula el promedio semanal de una ciudad.

    Parámetros:
        temperaturas_ciudad: lista de temperaturas diarias.

    Retorna:
        Promedio semanal.
    """
    suma = 0.0

    for temp in temperaturas_ciudad:
        suma += temp

    return suma / len(temperaturas_ciudad)
# Función 3: Procesamiento general y salida
def mostrar_promedios(ciudades: List[str], temperaturas: List[List[float]]) -> None:
    """
    Calcula e imprime el promedio semanal de cada ciudad.
    """
    for i in range(len(ciudades)):
        promedio = calcular_promedio_semanal(temperaturas[i])
        print(f"Ciudad: {ciudades[i]} -> Promedio semanal: {promedio:.2f} °C")

# Programa principal
if __name__ == "__main__":
    ciudades: List[str] = ["Guayaquil", "Cuenca", "Loja"]

    # Entrada de datos diarios
    temperaturas = ingresar_temperaturas(ciudades)

    # Cálculo y presentación de resultados
    print("\n--- PROMEDIOS SEMANALES ---")
    mostrar_promedios(ciudades, temperaturas)
