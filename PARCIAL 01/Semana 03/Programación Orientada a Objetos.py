# python
class ClimaCiudad:
    def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0, altitud: int = 0, nubosidad: float = 0.0) -> None:
        self._nombre: str = nombre
        self._dias_por_semana: int = dias_por_semana
        self._temp_base: float = temp_base
        self._altitud: int = altitud
        self._nubosidad: float = max(0.0, min(1.0, nubosidad))
        self._temperaturas: List[float] = []

    def ingresar_datos(self) -> None:
        self._temperaturas = []
        print(f"\nIngreso de temperaturas para: {self._nombre}")
        for dia in range(1, self._dias_por_semana + 1):
            while True:
                entrada = input(f"  Día {dia} - temperatura (°C): ").strip()
                try:
                    valor = float(entrada)
                    self._temperaturas.append(valor)
                    break
                except ValueError:
                    print("  Entrada inválida. Ingrese un número (ej: 19.5).")

    def promedio_semana(self) -> float:
        if not self._temperaturas:
            return float("nan")
        return sum(self._temperaturas) / len(self._temperaturas)
# python
from typing import List
import math

class ClimaCiudad:
    def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                 altitud: int = 0, nubosidad: float = 0.0) -> None:
        self._nombre: str = nombre
        self._dias_por_semana: int = dias_por_semana
        self._temp_base: float = temp_base
        self._altitud: int = altitud
        self._nubosidad: float = max(0.0, min(1.0, nubosidad))
        self._temperaturas: List[float] = []

    def ingresar_datos(self) -> None:
        self._temperaturas = []
        print(f"\nIngreso de temperaturas para: {self._nombre}")
        for dia in range(1, self._dias_por_semana + 1):
            while True:
                entrada = input(f"  Día {dia} - temperatura (°C): ").strip()
                try:
                    valor = float(entrada)
                    self._temperaturas.append(valor)
                    break
                except ValueError:
                    print("  Entrada inválida. Ingrese un número (ej: 19.5).")

    def promedio_semana(self) -> float:
        if not self._temperaturas:
            return float("nan")
        return sum(self._temperaturas) / len(self._temperaturas)

    def atributos(self) -> None:
        print(f"{self._nombre}: temp_base={self._temp_base}°C, altitud={self._altitud}msnm, "
              f"nubosidad={self._nubosidad}, días={self._dias_por_semana}")

    @property
    def nombre(self) -> str:
        return self._nombre


class CiudadCostera(ClimaCiudad):
    def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                 altitud: int = 0, nubosidad: float = 0.0, brisa: float = 1.10) -> None:
        super().__init__(nombre, dias_por_semana, temp_base, altitud, nubosidad)
        self._brisa: float = brisa  # factor fijo aplicado al promedio

    def promedio_semana(self) -> float:
        base = super().promedio_semana()
        if math.isnan(base):
            return base
        return base * self._brisa

    def atributos(self) -> None:
        super().atributos()
        print(f"  (costera) factor brisa={self._brisa}")


class CiudadAndina(ClimaCiudad):
    def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                 altitud: int = 0, nubosidad: float = 0.0) -> None:
        super().__init__(nombre, dias_por_semana, temp_base, altitud, nubosidad)

    def promedio_semana(self) -> float:
        base = super().promedio_semana()
        if math.isnan(base):
            return base
        ajuste = (self._altitud / 1000.0) * 0.6  # descenso aproximado por altitud
        return base - ajuste

    def atributos(self) -> None:
        super().atributos()
        print(f"  (andina) altitud={self._altitud}msnm, aplica ajuste -0.6°C/1000m")


class ClimaManager:
    def __init__(self, ciudades: List[ClimaCiudad]) -> None:
        self._ciudades = ciudades

    def ejecutar_registro(self) -> None:
        for c in self._ciudades:
            c.atributos()
        for c in self._ciudades:
            c.ingresar_datos()
        self.imprimir_resumen()
        self.comparar_pares()

    def imprimir_resumen(self) -> None:
        print("\n--- Resumen de promedios ---")
        for c in self._ciudades:
            p = c.promedio_semana()
            p_str = f"{p:.2f} °C" if not math.isnan(p) else "N/A"
            print(f"  {c.nombre}: {p_str}")

    def comparar_pares(self) -> None:
        print("\n--- Comparaciones por pares ---")
        n = len(self._ciudades)
        for i in range(n):
            for j in range(i + 1, n):
                a = self._ciudades[i]
                b = self._ciudades[j]
                pa = a.promedio_semana()
                pb = b.promedio_semana()
                pa_str = f"{pa:.2f}" if not math.isnan(pa) else "N/A"
                pb_str = f"{pb:.2f}" if not math.isnan(pb) else "N/A"
                print(f"{a.nombre} ({pa_str} °C) vs {b.nombre} ({pb_str} °C): ", end="")
                if math.isnan(pa) or math.isnan(pb):
                    print("Datos incompletos")
                elif pa > pb:
                    print(f"Mayor promedio: {a.nombre}")
                elif pb > pa:
                    print(f"Mayor promedio: {b.nombre}")
                else:
                    print("Empate")


if __name__ == "__main__":
    guayaquil = CiudadCostera("Guayaquil", dias_por_semana=7, temp_base=27.5, altitud=4, nubosidad=0.6, brisa=1.10)
    cuenca = CiudadAndina("Cuenca", dias_por_semana=7, temp_base=18.5, altitud=2560, nubosidad=0.5)
    loja = CiudadAndina("Loja", dias_por_semana=7, temp_base=18.0, altitud=2060, nubosidad=0.55)

    manager = ClimaManager([guayaquil, cuenca, loja])
    manager.ejecutar_registro()# python
    from typing import List
    import math

    class ClimaCiudad:
        def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                     altitud: int = 0, nubosidad: float = 0.0) -> None:
            self._nombre: str = nombre
            self._dias_por_semana: int = dias_por_semana
            self._temp_base: float = temp_base
            self._altitud: int = altitud
            self._nubosidad: float = max(0.0, min(1.0, nubosidad))
            self._temperaturas: List[float] = []

        def ingresar_datos(self) -> None:
            self._temperaturas = []
            print(f"\nIngreso de temperaturas para: {self._nombre}")
            for dia in range(1, self._dias_por_semana + 1):
                while True:
                    entrada = input(f"  Día {dia} - temperatura (°C): ").strip()
                    try:
                        valor = float(entrada)
                        self._temperaturas.append(valor)
                        break
                    except ValueError:
                        print("  Entrada inválida. Ingrese un número (ej: 19.5).")

        def promedio_semana(self) -> float:
            if not self._temperaturas:
                return float("nan")
            return sum(self._temperaturas) / len(self._temperaturas)

        def atributos(self) -> None:
            print(f"{self._nombre}: temp_base={self._temp_base}°C, altitud={self._altitud}msnm, "
                  f"nubosidad={self._nubosidad}, días={self._dias_por_semana}")

        @property
        def nombre(self) -> str:
            return self._nombre


    class CiudadCostera(ClimaCiudad):
        def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                     altitud: int = 0, nubosidad: float = 0.0, brisa: float = 1.10) -> None:
            super().__init__(nombre, dias_por_semana, temp_base, altitud, nubosidad)
            self._brisa: float = brisa  # factor fijo aplicado al promedio

        def promedio_semana(self) -> float:
            base = super().promedio_semana()
            if math.isnan(base):
                return base
            return base * self._brisa

        def atributos(self) -> None:
            super().atributos()
            print(f"  (costera) factor brisa={self._brisa}")


    class CiudadAndina(ClimaCiudad):
        def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                     altitud: int = 0, nubosidad: float = 0.0) -> None:
            super().__init__(nombre, dias_por_semana, temp_base, altitud, nubosidad)

        def promedio_semana(self) -> float:
            base = super().promedio_semana()
            if math.isnan(base):
                return base
            ajuste = (self._altitud / 1000.0) * 0.6  # descenso aproximado por altitud
            return base - ajuste

        def atributos(self) -> None:
            super().atributos()
            print(f"  (andina) altitud={self._altitud}msnm, aplica ajuste -0.6°C/1000m")


    class ClimaManager:
        def __init__(self, ciudades: List[ClimaCiudad]) -> None:
            self._ciudades = ciudades

        def ejecutar_registro(self) -> None:
            for c in self._ciudades:
                c.atributos()
            for c in self._ciudades:
                c.ingresar_datos()
            self.imprimir_resumen()
            self.comparar_pares()

        def imprimir_resumen(self) -> None:
            print("\n--- Resumen de promedios ---")
            for c in self._ciudades:
                p = c.promedio_semana()
                p_str = f"{p:.2f} °C" if not math.isnan(p) else "N/A"
                print(f"  {c.nombre}: {p_str}")

        def comparar_pares(self) -> None:
            print("\n--- Comparaciones por pares ---")
            n = len(self._ciudades)
            for i in range(n):
                for j in range(i + 1, n):
                    a = self._ciudades[i]
                    b = self._ciudades[j]
                    pa = a.promedio_semana()
                    pb = b.promedio_semana()
                    pa_str = f"{pa:.2f}" if not math.isnan(pa) else "N/A"
                    pb_str = f"{pb:.2f}" if not math.isnan(pb) else "N/A"
                    print(f"{a.nombre} ({pa_str} °C) vs {b.nombre} ({pb_str} °C): ", end="")
                    if math.isnan(pa) or math.isnan(pb):
                        print("Datos incompletos")
                    elif pa > pb:
                        print(f"Mayor promedio: {a.nombre}")
                    elif pb > pa:
                        print(f"Mayor promedio: {b.nombre}")
                    else:
                        print("Empate")


    if __name__ == "__main__":
        guayaquil = CiudadCostera("Guayaquil", dias_por_semana=7, temp_base=27.5, altitud=4, nubosidad=0.6, brisa=1.10)
        cuenca = CiudadAndina("Cuenca", dias_por_semana=7, temp_base=18.5, altitud=2560, nubosidad=0.5)
        loja = CiudadAndina("Loja", dias_por_semana=7, temp_base=18.0, altitud=2060, nubosidad=0.55)

        manager = ClimaManager([guayaquil, cuenca, loja])
        manager.ejecutar_registro()
    def atributos(self) -> None:
        print(f"{self._nombre}: temp_base={self._temp_base}°C, altitud={self._altitud}msnm, nubosidad={self._nubosidad}, días={self._dias_por_semana}")

    @property
    def nombre(self) -> str:
        return self._nombre# python
        from typing import List
        import math

        class ClimaCiudad:
            def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                         altitud: int = 0, nubosidad: float = 0.0) -> None:
                self._nombre: str = nombre
                self._dias_por_semana: int = dias_por_semana
                self._temp_base: float = temp_base
                self._altitud: int = altitud
                self._nubosidad: float = max(0.0, min(1.0, nubosidad))
                self._temperaturas: List[float] = []

            def ingresar_datos(self) -> None:
                self._temperaturas = []
                print(f"\nIngreso de temperaturas para: {self._nombre}")
                for dia in range(1, self._dias_por_semana + 1):
                    while True:
                        entrada = input(f"  Día {dia} - temperatura (°C): ").strip()
                        try:
                            valor = float(entrada)
                            self._temperaturas.append(valor)
                            break
                        except ValueError:
                            print("  Entrada inválida. Ingrese un número (ej: 19.5).")

            def promedio_semana(self) -> float:
                if not self._temperaturas:
                    return float("nan")
                return sum(self._temperaturas) / len(self._temperaturas)

            def atributos(self) -> None:
                print(f"{self._nombre}: temp_base={self._temp_base}°C, altitud={self._altitud}msnm, "
                      f"nubosidad={self._nubosidad}, días={self._dias_por_semana}")

            @property
            def nombre(self) -> str:
                return self._nombre


        class CiudadCostera(ClimaCiudad):
            def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                         altitud: int = 0, nubosidad: float = 0.0, brisa: float = 1.10) -> None:
                super().__init__(nombre, dias_por_semana, temp_base, altitud, nubosidad)
                self._brisa: float = brisa  # factor fijo aplicado al promedio

            def promedio_semana(self) -> float:
                base = super().promedio_semana()
                if math.isnan(base):
                    return base
                return base * self._brisa

            def atributos(self) -> None:
                super().atributos()
                print(f"  (costera) factor brisa={self._brisa}")


        class CiudadAndina(ClimaCiudad):
            def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                         altitud: int = 0, nubosidad: float = 0.0) -> None:
                super().__init__(nombre, dias_por_semana, temp_base, altitud, nubosidad)

            def promedio_semana(self) -> float:
                base = super().promedio_semana()
                if math.isnan(base):
                    return base
                ajuste = (self._altitud / 1000.0) * 0.6  # descenso aproximado por altitud
                return base - ajuste

            def atributos(self) -> None:
                super().atributos()
                print(f"  (andina) altitud={self._altitud}msnm, aplica ajuste -0.6°C/1000m")


        class ClimaManager:
            def __init__(self, ciudades: List[ClimaCiudad]) -> None:
                self._ciudades = ciudades

            def ejecutar_registro(self) -> None:
                for c in self._ciudades:
                    c.atributos()
                for c in self._ciudades:
                    c.ingresar_datos()
                self.imprimir_resumen()
                self.comparar_pares()

            def imprimir_resumen(self) -> None:
                print("\n--- Resumen de promedios ---")
                for c in self._ciudades:
                    p = c.promedio_semana()
                    p_str = f"{p:.2f} °C" if not math.isnan(p) else "N/A"
                    print(f"  {c.nombre}: {p_str}")

            def comparar_pares(self) -> None:
                print("\n--- Comparaciones por pares ---")
                n = len(self._ciudades)
                for i in range(n):
                    for j in range(i + 1, n):
                        a = self._ciudades[i]
                        b = self._ciudades[j]
                        pa = a.promedio_semana()
                        pb = b.promedio_semana()
                        pa_str = f"{pa:.2f}" if not math.isnan(pa) else "N/A"
                        pb_str = f"{pb:.2f}" if not math.isnan(pb) else "N/A"
                        print(f"{a.nombre} ({pa_str} °C) vs {b.nombre} ({pb_str} °C): ", end="")
                        if math.isnan(pa) or math.isnan(pb):
                            print("Datos incompletos")
                        elif pa > pb:
                            print(f"Mayor promedio: {a.nombre}")
                        elif pb > pa:
                            print(f"Mayor promedio: {b.nombre}")
                        else:
                            print("Empate")


        if __name__ == "__main__":
            guayaquil = CiudadCostera("Guayaquil", dias_por_semana=7, temp_base=27.5, altitud=4, nubosidad=0.6, brisa=1.10)
            cuenca = CiudadAndina("Cuenca", dias_por_semana=7, temp_base=18.5, altitud=2560, nubosidad=0.5)
            loja = CiudadAndina("Loja", dias_por_semana=7, temp_base=18.0, altitud=2060, nubosidad=0.55)

            manager = ClimaManager([guayaquil, cuenca, loja])
            manager.ejecutar_registro()# python
            from typing import List
            import math

            class ClimaCiudad:
                def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                             altitud: int = 0, nubosidad: float = 0.0) -> None:
                    self._nombre: str = nombre
                    self._dias_por_semana: int = dias_por_semana
                    self._temp_base: float = temp_base
                    self._altitud: int = altitud
                    self._nubosidad: float = max(0.0, min(1.0, nubosidad))
                    self._temperaturas: List[float] = []

                def ingresar_datos(self) -> None:
                    self._temperaturas = []
                    print(f"\nIngreso de temperaturas para: {self._nombre}")
                    for dia in range(1, self._dias_por_semana + 1):
                        while True:
                            entrada = input(f"  Día {dia} - temperatura (°C): ").strip()
                            try:
                                valor = float(entrada)
                                self._temperaturas.append(valor)
                                break
                            except ValueError:
                                print("  Entrada inválida. Ingrese un número (ej: 19.5).")

                def promedio_semana(self) -> float:
                    if not self._temperaturas:
                        return float("nan")
                    return sum(self._temperaturas) / len(self._temperaturas)

                def atributos(self) -> None:
                    print(f"{self._nombre}: temp_base={self._temp_base}°C, altitud={self._altitud}msnm, "
                          f"nubosidad={self._nubosidad}, días={self._dias_por_semana}")

                @property
                def nombre(self) -> str:
                    return self._nombre


            class CiudadCostera(ClimaCiudad):
                def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                             altitud: int = 0, nubosidad: float = 0.0, brisa: float = 1.10) -> None:
                    super().__init__(nombre, dias_por_semana, temp_base, altitud, nubosidad)
                    self._brisa: float = brisa  # factor fijo aplicado al promedio

                def promedio_semana(self) -> float:
                    base = super().promedio_semana()
                    if math.isnan(base):
                        return base
                    return base * self._brisa

                def atributos(self) -> None:
                    super().atributos()
                    print(f"  (costera) factor brisa={self._brisa}")


            class CiudadAndina(ClimaCiudad):
                def __init__(self, nombre: str, dias_por_semana: int = 7, temp_base: float = 0.0,
                             altitud: int = 0, nubosidad: float = 0.0) -> None:
                    super().__init__(nombre, dias_por_semana, temp_base, altitud, nubosidad)

                def promedio_semana(self) -> float:
                    base = super().promedio_semana()
                    if math.isnan(base):
                        return base
                    ajuste = (self._altitud / 1000.0) * 0.6  # descenso aproximado por altitud
                    return base - ajuste

                def atributos(self) -> None:
                    super().atributos()
                    print(f"  (andina) altitud={self._altitud}msnm, aplica ajuste -0.6°C/1000m")


            class ClimaManager:
                def __init__(self, ciudades: List[ClimaCiudad]) -> None:
                    self._ciudades = ciudades

                def ejecutar_registro(self) -> None:
                    for c in self._ciudades:
                        c.atributos()
                    for c in self._ciudades:
                        c.ingresar_datos()
                    self.imprimir_resumen()
                    self.comparar_pares()

                def imprimir_resumen(self) -> None:
                    print("\n--- Resumen de promedios ---")
                    for c in self._ciudades:
                        p = c.promedio_semana()
                        p_str = f"{p:.2f} °C" if not math.isnan(p) else "N/A"
                        print(f"  {c.nombre}: {p_str}")

                def comparar_pares(self) -> None:
                    print("\n--- Comparaciones por pares ---")
                    n = len(self._ciudades)
                    for i in range(n):
                        for j in range(i + 1, n):
                            a = self._ciudades[i]
                            b = self._ciudades[j]
                            pa = a.promedio_semana()
                            pb = b.promedio_semana()
                            pa_str = f"{pa:.2f}" if not math.isnan(pa) else "N/A"
                            pb_str = f"{pb:.2f}" if not math.isnan(pb) else "N/A"
                            print(f"{a.nombre} ({pa_str} °C) vs {b.nombre} ({pb_str} °C): ", end="")
                            if math.isnan(pa) or math.isnan(pb):
                                print("Datos incompletos")
                            elif pa > pb:
                                print(f"Mayor promedio: {a.nombre}")
                            elif pb > pa:
                                print(f"Mayor promedio: {b.nombre}")
                            else:
                                print("Empate")


            if __name__ == "__main__":
                guayaquil = CiudadCostera("Guayaquil", dias_por_semana=7, temp_base=27.5, altitud=4, nubosidad=0.6, brisa=1.10)
                cuenca = CiudadAndina("Cuenca", dias_por_semana=7, temp_base=18.5, altitud=2560, nubosidad=0.5)
                loja = CiudadAndina("Loja", dias_por_semana=7, temp_base=18.0, altitud=2060, nubosidad=0.55)

                manager = ClimaManager([guayaquil, cuenca, loja])
                manager.ejecutar_registro()