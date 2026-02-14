from producto import Producto
from typing import List, Optional


class Inventario:
    """
    Gestiona la colección de productos de la tienda.
    Utiliza una lista + diccionario para acceso rápido por ID.
    """

    def __init__(self):
        self._productos: List[Producto] = []
        self._indice_por_id: dict[int, Producto] = {}  # Para búsqueda O(1) por ID

    def agregar_producto(self, producto: Producto) -> bool:
        """Añade un producto si el ID no existe ya"""
        if producto.id in self._indice_por_id:
            print(f"¡Error! Ya existe un producto con ID {producto.id}")
            return False

        self._productos.append(producto)
        self._indice_por_id[producto.id] = producto
        print(f"Producto '{producto.nombre}' (ID: {producto.id}) agregado correctamente.")
        return True

    def eliminar_producto(self, id_producto: int) -> bool:
        """Elimina producto por ID"""
        if id_producto not in self._indice_por_id:
            print(f"No se encontró producto con ID {id_producto}")
            return False

        producto = self._indice_por_id.pop(id_producto)
        self._productos.remove(producto)
        print(f"Producto '{producto.nombre}' (ID: {id_producto}) eliminado.")
        return True

    def actualizar_cantidad(self, id_producto: int, nueva_cantidad: int) -> bool:
        """Actualiza solo la cantidad de un producto"""
        producto = self._indice_por_id.get(id_producto)
        if producto is None:
            print(f"No se encontró producto con ID {id_producto}")
            return False

        try:
            producto.cantidad = nueva_cantidad
            print(f"Cantidad actualizada → {producto}")
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def actualizar_precio(self, id_producto: int, nuevo_precio: float) -> bool:
        """Actualiza solo el precio de un producto"""
        producto = self._indice_por_id.get(id_producto)
        if producto is None:
            print(f"No se encontró producto con ID {id_producto}")
            return False

        try:
            producto.precio = nuevo_precio
            print(f"Precio actualizado → {producto}")
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def buscar_por_nombre(self, texto: str) -> List[Producto]:
        """Búsqueda parcial por nombre (insensible a mayúsculas)"""
        texto = texto.lower().strip()
        resultados = [p for p in self._productos if texto in p.nombre.lower()]
        return resultados

    def mostrar_todos(self) -> None:
        """Muestra todos los productos ordenados por nombre"""
        if not self._productos:
            print("El inventario está vacío.")
            return

        print("\n" + "═" * 70)
        print(f"{'ID':4}  {'Nombre':25}  {'Cant.':6}  {'Precio':8}")
        print("─" * 70)

        # Ordenamos por nombre para mejor visualización
        for producto in sorted(self._productos, key=lambda p: p.nombre):
            print(producto)
        print("═" * 70)

    def contar_productos(self) -> int:
        return len(self._productos)

