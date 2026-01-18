# ===============================
# Clase base / Clase padre
# ===============================
class Mascota:
    """
    Clase base que representa una mascota.
    Aplica encapsulamiento y define un metodo polimórfico.
    """

    def __init__(self, nombre: str, edad: int):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if edad < 0:
            raise ValueError("La edad no puede ser negativa")

        self.__nombre = nombre      # Encapsulación (atributo privado)
        self.__edad = edad

    # Métodos de encapsulación
    def get_nombre(self) -> str:
        return self.__nombre

    def get_edad(self) -> int:
        return self.__edad

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def edad(self) -> int:
        return self.__edad

    # Metodo polimorfismo
    def mostrar_informacion(self) -> str:
        return "Información de la mascota"


# ===============================
# Clase hija de nuestro Perro
# ===============================
class Perro(Mascota):
    def __init__(self, nombre: str, edad: int, raza: str):
        super().__init__(nombre, edad)
        self.raza = raza

    def mostrar_informacion(self) -> str:
        return (
            f" Tipo  : Perro\n"
            f" Nombre: {self.get_nombre()}\n"
            f" Edad  : {self.get_edad()} años\n"
            f" Raza  : {self.raza}"
        )


# ===============================
# Clase hija de nuestro Gato
# ===============================
class Gato(Mascota):
    def __init__(self, nombre: str, edad: int, color: str):
        super().__init__(nombre, edad)
        self.color = color

    def mostrar_informacion(self) -> str:
        return (
            f" Tipo  : Gato\n"
            f" Nombre: {self.get_nombre()}\n"
            f" Edad  : {self.get_edad()} años\n"
            f" Color : {self.color}"
        )


# ===============================
# El programa principal
# ===============================
if __name__ == "__main__":

    print("=" * 40)
    print("      REGISTRO DE MASCOTAS ")
    print("=" * 40)

    # Definir los objetos
    mi_perro = Perro("Rocky", 4, "Dálmata")
    mi_gato = Gato("Dorami", 1, "Gris")

    # Información con formato estético
    print("\n" + "-" * 40)
    print(mi_perro.mostrar_informacion())
    print("-" * 40)

    print("\n" + "-" * 40)
    print(mi_gato.mostrar_informacion())
    print("-" * 40)