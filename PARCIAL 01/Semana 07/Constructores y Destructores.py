import gc

class Animal:
    def __init__(self, nombre, especie, edad):
        # Constructor: inicializa atributos del objeto
        self.nombre = nombre
        self.especie = especie
        self.edad = edad
        self.adoptado = False
        print(f"Constructor Animal creado: {self}")

    def adoptar(self):
        if not self.adoptado:
            self.adoptado = True
            print(f"{self.nombre} ha sido adoptado.")
        else:
            print(f"{self.nombre} ya estaba adoptado.")

    def __repr__(self):
        return f"{self.nombre} ({self.especie}, {self.edad} años)"

    def __del__(self):
        # Destructor: se activa cuando el objeto se elimina/recolecta
        print(f"Destructor Liberando recursos de: {self}")


class Refugio:
    def __init__(self, nombre):
        # Constructor del refugio
        self.nombre = nombre
        self.animales = []
        print(f"Constructor  ----  Refugio '{self.nombre}' creado.")

    def recibir(self, animal):
        self.animales.append(animal)
        print(f"{animal} recibido en {self.nombre}.")

    def listar(self):
        for a in self.animales:
            estado = "Adoptado" if a.adoptado else "Disponible"
            print(f"- {a}: {estado}")

    def __del__(self):
        # Destructor del refugio: limpieza de referencias
        print(f"Destructor  ---- Cerrando refugio '{self.nombre}' y liberando referencias.")
        self.animales.clear()


if __name__ == "__main__":
    r = Refugio("centro de Ayuda Pets")
    a1 = Animal("Rocky", "Perro", 4)
    a2 = Animal("Minina", "Gato", 1)

    r.recibir(a1)
    r.recibir(a2)

    print("\nListado inicial:")
    r.listar()

    print("\nAdoptando a Rocky:")
    a1.adoptar()

    print("\nListado tras adopción:")
    r.listar()

    # Eliminamos una referencia y forzamos recolección para ver el destructor en acción
    print("\nEliminando la referencia a 'Misi' y forzando recolección:")
    del a2
    gc.collect()

    print("\nFin del programa  ----  Al cerrar se llamarán los destructores restantes).")