import random

class Personaje:
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida):
        self.nombre = nombre
        self.fuerza = fuerza
        self.inteligencia = inteligencia
        self.defensa = defensa
        self._vida = vida

    # Propiedad vida segura
    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor):
        self._vida = max(0, valor)

    # Métodos base
    def atributos(self):
        print(f"\n{self.nombre} — Atributos")
        print(f"  Fuerza:       {self.fuerza}")
        print(f"  Inteligencia: {self.inteligencia}")
        print(f"  Defensa:      {self.defensa}")
        print(f"  Vida:         {self.vida}")

    def esta_vivo(self):
        return self.vida > 0

    def morir(self):
        print(f"💀 {self.nombre} ha muerto.")

    # Cálculo de daño base
    def daño(self, enemigo):
        raise NotImplementedError("Este personaje aún no define daño.")

    # Nuevo sistema de combate (críticos + evasión)
    def ataque_final(self, enemigo, daño_base):
        crítico = random.random() < 0.15
        evasion = random.random() < 0.10

        if evasion:
            print(f"⚡ {enemigo.nombre} esquivó el ataque!")
            return 0

        if crítico:
            print(f"🔥 ¡Golpe crítico de {self.nombre}!")
            daño_base *= 1.5

        daño_final = max(0, daño_base - enemigo.defensa)
        enemigo.vida -= daño_final

        return daño_final

    def atacar(self, enemigo):
        daño_base = self.daño(enemigo)
        daño_hecho = self.ataque_final(enemigo, daño_base)

        print(f"{self.nombre} inflige {daño_hecho:.1f} de daño a {enemigo.nombre}")

        if not enemigo.esta_vivo():
            enemigo.morir()


# =========================
#   CLASE GUERRERO
# =========================
class Guerrero(Personaje):
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida, espada):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida)
        self.espada = espada  # Daño del arma

    def daño(self, enemigo):
        return self.fuerza * (1 + self.espada / 10)

    def atributos(self):
        super().atributos()
        print(f"  Espada:       {self.espada}")


# =========================
#   CLASE MAGO
# =========================
class Mago(Personaje):
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida, libro):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida)
        self.libro = libro  # Potencia mágica

    def daño(self, enemigo):
        return self.inteligencia * (1 + self.libro / 10)

    def atributos(self):
        super().atributos()
        print(f"  Grimorio:     {self.libro}")


# =========================
#   MOTOR DE COMBATE
# =========================
def combate(j1, j2):
    turno = 1
    print("\n⚔️ ¡COMIENZA EL COMBATE! ⚔️")

    while j1.esta_vivo() and j2.esta_vivo():
        print(f"\n====== Turno {turno} ======")
        j1.atacar(j2)
        if j2.esta_vivo():
            j2.atacar(j1)
        turno += 1

    print("\n🏁 Fin del combate")
    if j1.esta_vivo():
        print(f"🏆 {j1.nombre} es el ganador!")
    elif j2.esta_vivo():
        print(f"🏆 {j2.nombre} es la ganadora!")
    else:
        print("🤝 Ambos han caído. ¡Empate!")


# =========================
#     EJEMPLO DE USO
# =========================

aldric = Guerrero("Aldric el Alto", 20, 8, 5, 120, espada=12)
lyssandra = Mago("Lyssandra la Arcana", 6, 18, 4, 100, libro=10)

aldric.atributos()
lyssandra.atributos()

combate(aldric, lyssandra)
