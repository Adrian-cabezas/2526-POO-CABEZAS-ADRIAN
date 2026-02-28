"""
inventario.py
=============
Define la clase Inventario que gestiona la colección de productos.

Colecciones utilizadas:
    - Diccionario (dict) : almacenamiento principal {id: Producto}, permite
                           búsqueda, inserción y eliminación en O(1).
    - Conjunto (set)     : control rápido de IDs existentes, evita duplicados.
    - Lista (list)       : resultados de búsquedas por nombre.
    - Tupla (tuple)      : representación inmutable al verificar integridad.
"""

import json
import os

from producto import Producto


class Inventario:
    """
    Gestiona la colección completa de productos del inventario.
    Implementa operaciones CRUD y almacenamiento persistente en JSON.
    """

    ARCHIVO_INVENTARIO = "inventario.json"

    def __init__(self):
        """
        Inicializa el inventario con las colecciones necesarias:
            - __productos      : diccionario principal {id: Producto}
            - __ids_existentes : conjunto de IDs para control de unicidad
        """
        # Diccionario: acceso directo a cualquier producto por su ID
        self.__productos: dict[str, Producto] = {}
        # Conjunto: verificación O(1) de IDs duplicados
        self.__ids_existentes: set[str] = set()

    # ─────────────────────────────────────────
    # AÑADIR
    # ─────────────────────────────────────────

    def añadir_producto(self, producto: Producto) -> bool:
        """
        Añade un nuevo producto al inventario.
        Usa el conjunto de IDs para detectar duplicados eficientemente.
        Retorna True si se añadió correctamente, False si el ID ya existe.
        """
        pid = producto.get_id()
        if pid in self.__ids_existentes:
            print(f"  ✗ Ya existe un producto con el ID '{pid}'.")
            return False
        self.__productos[pid] = producto
        self.__ids_existentes.add(pid)
        print(f"  ✓ Producto '{producto.get_nombre()}' añadido correctamente.")
        return True

    # ─────────────────────────────────────────
    # ELIMINAR
    # ─────────────────────────────────────────

    def eliminar_producto(self, producto_id: str) -> bool:
        """
        Elimina un producto del inventario por su ID.
        Retorna True si se eliminó, False si el ID no existe.
        """
        if producto_id not in self.__ids_existentes:
            print(f"  ✗ No se encontró ningún producto con ID '{producto_id}'.")
            return False
        nombre = self.__productos[producto_id].get_nombre()
        del self.__productos[producto_id]
        self.__ids_existentes.discard(producto_id)
        print(f"  ✓ Producto '{nombre}' (ID: {producto_id}) eliminado.")
        return True

    # ─────────────────────────────────────────
    # ACTUALIZAR
    # ─────────────────────────────────────────

    def actualizar_producto(
        self,
        producto_id: str,
        nueva_cantidad: int = None,
        nuevo_precio: float = None,
    ) -> bool:
        """
        Actualiza la cantidad y/o el precio de un producto existente.
        Retorna True si se actualizó, False si el ID no existe.
        """
        if producto_id not in self.__ids_existentes:
            print(f"  ✗ No se encontró ningún producto con ID '{producto_id}'.")
            return False
        producto = self.__productos[producto_id]
        if nueva_cantidad is not None:
            producto.set_cantidad(nueva_cantidad)
        if nuevo_precio is not None:
            producto.set_precio(nuevo_precio)
        print(f"  ✓ Producto '{producto.get_nombre()}' actualizado correctamente.")
        return True

    # ─────────────────────────────────────────
    # BUSCAR POR NOMBRE
    # ─────────────────────────────────────────

    def buscar_por_nombre(self, nombre: str) -> list:
        """
        Busca productos cuyo nombre contenga el texto indicado.
        La búsqueda es insensible a mayúsculas/minúsculas.
        Retorna una lista de objetos Producto que coincidan.
        """
        termino = nombre.lower().strip()
        # Comprensión de lista sobre los valores del diccionario
        resultados: list[Producto] = [
            p
            for p in self.__productos.values()
            if termino in p.get_nombre().lower()
        ]
        return resultados

    # ─────────────────────────────────────────
    # MOSTRAR PRODUCTO POR ID
    # ─────────────────────────────────────────

    def mostrar_producto(self, producto_id: str):
        """Muestra la información detallada de un producto por su ID."""
        if producto_id not in self.__ids_existentes:
            print(f"  ✗ No se encontró ningún producto con ID '{producto_id}'.")
            return
        print(self.__productos[producto_id])

    # ─────────────────────────────────────────
    # MOSTRAR TODOS
    # ─────────────────────────────────────────

    def mostrar_todos(self):
        """Muestra la información de todos los productos en el inventario."""
        if not self.__productos:
            print("  El inventario está vacío.")
            return
        separador = "─" * 40
        for producto in self.__productos.values():
            print(separador)
            print(producto)
        print(separador)
        print(f"  Total de productos: {len(self.__productos)}")

    # ─────────────────────────────────────────
    # GUARDAR EN ARCHIVO
    # ─────────────────────────────────────────

    def guardar_en_archivo(self, ruta: str = None):
        """
        Serializa el inventario completo a un archivo JSON.
        Convierte cada Producto a diccionario usando to_dict().
        Usa tuplas para verificar la integridad de los datos antes de guardar.
        """
        if ruta is None:
            ruta = self.ARCHIVO_INVENTARIO

        # Verificación de integridad mediante tuplas (colección inmutable)
        tuplas = [p.to_tupla() for p in self.__productos.values()]
        if len(tuplas) != len(self.__productos):
            print("  ✗ Error de integridad al preparar los datos.")
            return

        # Serialización del diccionario a JSON
        datos = [p.to_dict() for p in self.__productos.values()]
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            print(f"  ✓ Inventario guardado en '{ruta}' ({len(datos)} productos).")
        except OSError as e:
            print(f"  ✗ Error al guardar el archivo: {e}")

    # ─────────────────────────────────────────
    # CARGAR DESDE ARCHIVO
    # ─────────────────────────────────────────

    def cargar_desde_archivo(self, ruta: str = None):
        """
        Deserializa el inventario desde un archivo JSON.
        Reconstruye los objetos Producto usando from_dict().
        Reemplaza el inventario actual con los datos del archivo.
        """
        if ruta is None:
            ruta = self.ARCHIVO_INVENTARIO

        if not os.path.exists(ruta):
            print(f"  ✗ No se encontró el archivo '{ruta}'.")
            return

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos: list[dict] = json.load(f)

            # Reiniciar las colecciones antes de cargar
            self.__productos = {}
            self.__ids_existentes = set()

            for item in datos:
                producto = Producto.from_dict(item)
                self.__productos[producto.get_id()] = producto
                self.__ids_existentes.add(producto.get_id())

            print(f"  ✓ Inventario cargado desde '{ruta}' ({len(datos)} productos).")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"  ✗ Error al cargar el archivo: {e}")

    # ─────────────────────────────────────────
    # UTILIDADES
    # ─────────────────────────────────────────

    def __len__(self) -> int:
        """Retorna el número total de productos en el inventario."""
        return len(self.__productos)