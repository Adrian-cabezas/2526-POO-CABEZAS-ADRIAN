"""
producto.py
===========
Define la clase Producto con sus atributos y métodos.

Atributos:
    - id       : Identificador único del producto (str)
    - nombre   : Nombre del producto (str)
    - cantidad : Cantidad disponible en inventario (int)
    - precio   : Precio unitario del producto (float)
"""


class Producto:
    """
    Representa un producto dentro del inventario de la tienda.
    Utiliza atributos privados con getters y setters para
    garantizar la integridad de los datos.
    """

    def __init__(self, producto_id: str, nombre: str, cantidad: int, precio: float):
        """
        Constructor del producto.
        Parámetros:
            producto_id : ID único del producto
            nombre      : Nombre descriptivo del producto
            cantidad    : Cantidad inicial en inventario
            precio      : Precio unitario del producto
        """
        self.__id = producto_id
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # ─────────────────────────────────────────
    # GETTERS
    # ─────────────────────────────────────────

    def get_id(self) -> str:
        """Retorna el ID único del producto."""
        return self.__id

    def get_nombre(self) -> str:
        """Retorna el nombre del producto."""
        return self.__nombre

    def get_cantidad(self) -> int:
        """Retorna la cantidad disponible del producto."""
        return self.__cantidad

    def get_precio(self) -> float:
        """Retorna el precio unitario del producto."""
        return self.__precio

    # ─────────────────────────────────────────
    # SETTERS
    # ─────────────────────────────────────────

    def set_nombre(self, nombre: str):
        """Establece un nuevo nombre. No puede estar vacío."""
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = nombre.strip()

    def set_cantidad(self, cantidad: int):
        """Establece una nueva cantidad. No puede ser negativa."""
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = cantidad

    def set_precio(self, precio: float):
        """Establece un nuevo precio. No puede ser negativo."""
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = precio

    # ─────────────────────────────────────────
    # SERIALIZACIÓN
    # ─────────────────────────────────────────

    def to_dict(self) -> dict:
        """
        Convierte el producto a un diccionario.
        Utilizado para serialización en archivo JSON.
        """
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "cantidad": self.__cantidad,
            "precio": self.__precio,
        }

    def to_tupla(self) -> tuple:
        """
        Retorna una tupla inmutable con los datos del producto.
        Útil para verificar integridad antes de guardar.
        """
        return (self.__id, self.__nombre, self.__cantidad, self.__precio)

    @staticmethod
    def from_dict(data: dict) -> "Producto":
        """
        Crea un objeto Producto desde un diccionario.
        Utilizado para deserialización desde archivo JSON.
        """
        return Producto(
            data["id"],
            data["nombre"],
            int(data["cantidad"]),
            float(data["precio"]),
        )

    # ─────────────────────────────────────────
    # REPRESENTACIÓN
    # ─────────────────────────────────────────

    def __str__(self) -> str:
        """Representación legible del producto para mostrar en consola."""
        return (
            f"  ID       : {self.__id}\n"
            f"  Nombre   : {self.__nombre}\n"
            f"  Cantidad : {self.__cantidad}\n"
            f"  Precio   : ${self.__precio:.2f}"
        )