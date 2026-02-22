from producto import Producto
from inventario import Inventario


def mostrar_menu():
    print("\n" + "★" * 35)
    print("     SISTEMA DE GESTIÓN DE INVENTARIO")
    print("★" * 35)
    print("1. Agregar nuevo producto")
    print("2. Eliminar producto")
    print("3. Actualizar cantidad")
    print("4. Actualizar precio")
    print("5. Buscar producto(s) por nombre")
    print("6. Mostrar todos los productos")
    print("7. Salir")
    print("★" * 35)


def obtener_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Por favor ingrese un número entero válido.")


def obtener_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Por favor ingrese un número válido (puede tener decimales).")


def main():
    # Al instanciar Inventario, carga automáticamente los datos desde inventario.txt
    inventario = Inventario()

    # Datos de ejemplo: solo se cargan si el inventario está vacío
    # (es decir, si inventario.txt no existe o está vacío)
    if inventario.contar_productos() == 0:
        print("\n[INFO] Cargando datos de ejemplo en el inventario...")
        ejemplos = [
            Producto(1, "Laptop HP ProBook 444Os", 8, 750.99),
            Producto(2, "Mouse inalámbrico con RGB", 25, 19.90),
            Producto(3, "Teclado con pistones RGB", 14, 45.50),
            Producto(4, "Monitor 20 pulgadas", 6, 189.00),
            Producto(5, "Camara Sony ZV-E10", 6, 799.00),
            Producto(6, "Cpu Ryzen 5 5600", 6, 1109),
            Producto(7, "Primus Arcus100t ", 6, 37.83),
        ]
        for p in ejemplos:
            inventario.agregar_producto(p)

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-7): ").strip()

        if opcion == "1":
            id_prod  = obtener_entero("ID del producto: ")
            nombre   = input("Nombre del producto: ").strip()
            cantidad = obtener_entero("Cantidad en stock: ")
            precio   = obtener_float("Precio unitario ($): ")

            try:
                nuevo = Producto(id_prod, nombre, cantidad, precio)
                inventario.agregar_producto(nuevo)
            except ValueError as e:
                print(f"Error al crear producto: {e}")

        elif opcion == "2":
            id_prod = obtener_entero("ID del producto a eliminar: ")
            inventario.eliminar_producto(id_prod)

        elif opcion == "3":
            id_prod    = obtener_entero("ID del producto: ")
            nueva_cant = obtener_entero("Nueva cantidad: ")
            inventario.actualizar_cantidad(id_prod, nueva_cant)

        elif opcion == "4":
            id_prod      = obtener_entero("ID del producto: ")
            nuevo_precio = obtener_float("Nuevo precio ($): ")
            inventario.actualizar_precio(id_prod, nuevo_precio)

        elif opcion == "5":
            busqueda   = input("Ingrese texto a buscar en el nombre: ").strip()
            resultados = inventario.buscar_por_nombre(busqueda)
            if not resultados:
                print("No se encontraron productos con ese texto.")
            else:
                print(f"\nResultados encontrados ({len(resultados)}):")
                for p in resultados:
                    print(p)

        elif opcion == "6":
            inventario.mostrar_todos()

        elif opcion == "7":
            print("\n¡Gracias por usar el sistema de inventario!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()