class Producto:
    """
    Representa un producto en el inventario de la tienda.
    Cada producto tiene un ID único, nombre, cantidad en stock y precio unitario.
    """

    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        """
        Constructor del producto

        Args:
            id_producto: Identificador único (entero positivo)
            nombre: Nombre del producto
            cantidad: Cantidad disponible en stock (≥ 0)
            precio: Precio unitario (≥ 0)
        """
        if id_producto <= 0:
            raise ValueError("El ID debe ser un número entero positivo")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")

        self._id = id_producto
        self._nombre = nombre.strip().title()  # Normalizamos el nombre
        self._cantidad = cantidad
        self._precio = precio

    # Getters
    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def precio(self) -> float:
        return self._precio

    # Setters (solo para cantidad y precio, id y nombre no cambian)
    @cantidad.setter
    def cantidad(self, nueva_cantidad: int):
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self._cantidad = nueva_cantidad

    @precio.setter
    def precio(self, nuevo_precio: float):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = nuevo_precio

    def __str__(self) -> str:
        return (f"ID: {self._id:4d} | {self._nombre:25s} | "
                f"Cantidad: {self._cantidad:4d} | Precio: ${self._precio:7.2f}")

    def __repr__(self) -> str:
        return f"Producto(id={self._id}, nombre='{self._nombre}', cantidad={self._cantidad}, precio={self._precio})"