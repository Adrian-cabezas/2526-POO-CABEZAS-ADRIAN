"""
main.py
=======
Punto de entrada del Sistema de Gestión de Inventario.
Contiene el menú interactivo y todas las funciones de interfaz
que permiten al usuario operar sobre el inventario desde la consola.
"""

import os

from producto import Producto
from inventario import Inventario


# ─────────────────────────────────────────────
# FUNCIONES DE UTILIDAD
# ─────────────────────────────────────────────

def mostrar_menu():
    """Muestra el menú principal del sistema."""
    print("\n" + "═" * 45)
    print("    SISTEMA DE GESTIÓN DE INVENTARIO")
    print("═" * 45)
    print("  1. Añadir producto")
    print("  2. Eliminar producto")
    print("  3. Actualizar cantidad o precio")
    print("  4. Buscar productos por nombre")
    print("  5. Mostrar producto por ID")
    print("  6. Mostrar todos los productos")
    print("  7. Guardar inventario en archivo")
    print("  8. Cargar inventario desde archivo")
    print("  0. Salir")
    print("═" * 45)


def pedir_entero(prompt: str, minimo: int = 0) -> int:
    """
    Solicita un número entero al usuario con validación.
    Repite la solicitud hasta recibir un valor válido.
    """
    while True:
        try:
            valor = int(input(prompt))
            if valor < minimo:
                print(f"  ✗ El valor mínimo permitido es {minimo}.")
            else:
                return valor
        except ValueError:
            print("  ✗ Por favor, ingresa un número entero válido.")


def pedir_flotante(prompt: str, minimo: float = 0.0) -> float:
    """
    Solicita un número decimal al usuario con validación.
    Repite la solicitud hasta recibir un valor válido.
    """
    while True:
        try:
            valor = float(input(prompt))
            if valor < minimo:
                print(f"  ✗ El valor mínimo permitido es {minimo}.")
            else:
                return valor
        except ValueError:
            print("  ✗ Por favor, ingresa un número decimal válido.")


# ─────────────────────────────────────────────
# OPCIONES DEL MENÚ
# ─────────────────────────────────────────────

def opcion_añadir(inventario: Inventario):
    """Solicita los datos de un nuevo producto y lo añade al inventario."""
    print("\n── Añadir Producto ──")
    producto_id = input("  ID del producto  : ").strip()
    if not producto_id:
        print("  ✗ El ID no puede estar vacío.")
        return
    nombre = input("  Nombre           : ").strip()
    if not nombre:
        print("  ✗ El nombre no puede estar vacío.")
        return
    cantidad = pedir_entero("  Cantidad         : ")
    precio = pedir_flotante("  Precio ($)       : ")
    producto = Producto(producto_id, nombre, cantidad, precio)
    inventario.añadir_producto(producto)


def opcion_eliminar(inventario: Inventario):
    """Solicita el ID de un producto y lo elimina del inventario."""
    print("\n── Eliminar Producto ──")
    producto_id = input("  ID del producto a eliminar: ").strip()
    inventario.eliminar_producto(producto_id)


def opcion_actualizar(inventario: Inventario):
    """Permite actualizar la cantidad, el precio o ambos de un producto."""
    print("\n── Actualizar Producto ──")
    producto_id = input("  ID del producto a actualizar: ").strip()
    print("  ¿Qué deseas actualizar?")
    print("  1. Cantidad")
    print("  2. Precio")
    print("  3. Ambos")
    opcion = input("  Opción: ").strip()

    nueva_cantidad = None
    nuevo_precio = None

    if opcion in ("1", "3"):
        nueva_cantidad = pedir_entero("  Nueva cantidad   : ")
    if opcion in ("2", "3"):
        nuevo_precio = pedir_flotante("  Nuevo precio ($) : ")
    if opcion not in ("1", "2", "3"):
        print("  ✗ Opción inválida.")
        return

    inventario.actualizar_producto(producto_id, nueva_cantidad, nuevo_precio)


def opcion_buscar(inventario: Inventario):
    """Busca productos por nombre y muestra los resultados."""
    print("\n── Buscar por Nombre ──")
    termino = input("  Nombre o parte del nombre: ").strip()
    resultados = inventario.buscar_por_nombre(termino)
    if not resultados:
        print("  No se encontraron productos con ese nombre.")
    else:
        print(f"\n  Se encontraron {len(resultados)} resultado(s):")
        for producto in resultados:
            print("─" * 40)
            print(producto)


def opcion_mostrar_uno(inventario: Inventario):
    """Muestra la información detallada de un producto por su ID."""
    print("\n── Mostrar Producto por ID ──")
    producto_id = input("  ID del producto: ").strip()
    inventario.mostrar_producto(producto_id)


def opcion_guardar(inventario: Inventario):
    """Guarda el inventario en un archivo JSON."""
    print("\n── Guardar en Archivo ──")
    ruta = input("  Nombre del archivo [Enter para 'inventario.json']: ").strip()
    if not ruta:
        inventario.guardar_en_archivo()
    else:
        inventario.guardar_en_archivo(ruta)


def opcion_cargar(inventario: Inventario):
    """Carga el inventario desde un archivo JSON."""
    print("\n── Cargar desde Archivo ──")
    ruta = input("  Nombre del archivo [Enter para 'inventario.json']: ").strip()
    if not ruta:
        inventario.cargar_desde_archivo()
    else:
        inventario.cargar_desde_archivo(ruta)


# ─────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ─────────────────────────────────────────────

def main():
    """
    Función principal que inicializa el inventario y
    ejecuta el bucle del menú interactivo.
    """
    inventario = Inventario()

    # Carga automática si el archivo por defecto ya existe
    if os.path.exists(Inventario.ARCHIVO_INVENTARIO):
        print(f"\nArchivo '{Inventario.ARCHIVO_INVENTARIO}' encontrado. Cargando inventario...")
        inventario.cargar_desde_archivo()

    while True:
        mostrar_menu()
        opcion = input("  Selecciona una opción: ").strip()

        if opcion == "1":
            opcion_añadir(inventario)
        elif opcion == "2":
            opcion_eliminar(inventario)
        elif opcion == "3":
            opcion_actualizar(inventario)
        elif opcion == "4":
            opcion_buscar(inventario)
        elif opcion == "5":
            opcion_mostrar_uno(inventario)
        elif opcion == "6":
            print("\n── Todos los Productos ──")
            inventario.mostrar_todos()
        elif opcion == "7":
            opcion_guardar(inventario)
        elif opcion == "8":
            opcion_cargar(inventario)
        elif opcion == "0":
            print("\n  ¿Deseas guardar el inventario antes de salir? (s/n): ", end="")
            respuesta = input().strip().lower()
            if respuesta == "s":
                inventario.guardar_en_archivo()
            print("\n  ¡Hasta luego!\n")
            break
        else:
            print("  ✗ Opción no válida. Por favor selecciona una opción del menú.")

        input("\n  Presiona Enter para continuar...")


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()