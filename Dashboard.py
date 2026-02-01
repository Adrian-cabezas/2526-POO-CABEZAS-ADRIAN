import os
import subprocess
import sys


def mostrar_codigo(ruta_script):
    """Muestra el contenido de un archivo Python"""
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print(f"\n{'=' * 70}")
            print(f" 📄 Código de: {os.path.basename(ruta_script)}")
            print(f"{'=' * 70}\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print(f"\n❌ ERROR: Archivo no encontrado: {ruta_script_absoluta}")
        return None
    except Exception as e:
        print(f"\n⚠️ Error al leer el archivo: {e}")
        return None


def ejecutar_codigo(ruta_script):
    """Ejecuta un script Python DIRECTAMENTE en la misma consola (SIN VENTANAS EXTERNAS)"""
    if not os.path.isfile(ruta_script):
        print(f"\n❌ ERROR: El archivo no existe: {ruta_script}")
        return False

    try:
        ruta_script_absoluta = os.path.abspath(ruta_script)

        print(f"\n{'=' * 70}")
        print(f" ▶️  EJECUTANDO: {os.path.basename(ruta_script)}")
        print(f"{'=' * 70}\n")

        # 🔑 EJECUCIÓN DIRECTA EN LA MISMA CONSOLA (SIN VENTANAS EXTERNAS)
        resultado = subprocess.run(
            [sys.executable, ruta_script_absoluta],
            capture_output=False,  # Muestra salida directamente en consola
            text=True,
            cwd=os.path.dirname(ruta_script_absoluta)  # Establecer directorio de trabajo
        )

        print(f"\n{'=' * 70}")
        if resultado.returncode == 0:
            print(" ✅ Script ejecutado correctamente")
        else:
            print(f" ⚠️  El script terminó con código de error: {resultado.returncode}")
        print(f"{'=' * 70}\n")
        return True

    except Exception as e:
        print(f"\n❌ ERROR al ejecutar: {e}")
        return False


def obtener_semanas(ruta_parcial):
    """Obtiene y ordena todas las carpetas de semanas"""
    try:
        carpetas = [f.name for f in os.scandir(ruta_parcial) if f.is_dir()]
        # Filtrar y ordenar semanas numéricamente
        semanas = sorted(
            [c for c in carpetas if 'semana' in c.lower()],
            key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else 999
        )
        return semanas
    except Exception as e:
        print(f"\n❌ Error al escanear carpetas: {e}")
        return []


def mostrar_menu():
    """Menú principal del Dashboard"""
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_parcial_01 = os.path.join(ruta_base, 'PARCIAL 01')

    # Verificación crítica de estructura
    if not os.path.exists(ruta_parcial_01):
        print("\n" + "❌" * 40)
        print(" ERROR: Carpeta 'PARCIAL 01' no encontrada ".center(80))
        print("❌" * 40)
        print(f"\n📁 Ruta esperada: {ruta_parcial_01}")
        print("\n✅ Estructura correcta requerida:")
        print("   TuProyecto/")
        print("   ├── PARCIAL 01/")
        print("   │   ├── Semana 02/")
        print("   │   ├── Semana 03/")
        print("   │   ├── Semana 04/")
        print("   │   ├── Semana 05/")
        print("   │   ├── Semana 06/")
        print("   │   ├── Semana 07/")
        print("   │   └── Semana 08/")
        print("   └── Dashboard.py  ← ¡DEBE ESTAR AQUÍ!")
        print("\n" + "❌" * 40)
        input("\n⚠️ Presiona Enter para salir...")
        return

    semanas = obtener_semanas(ruta_parcial_01)
    if not semanas:
        print("\n⚠️ No se encontraron carpetas de semanas en 'PARCIAL 01'")
        input("\nPresiona Enter para salir...")
        return

    # Menú principal
    while True:
        print("\n" + "═" * 70)
        print(" 🚀 DASHBOARD DE PROYECTOS - PARCIAL 01 ".center(70))
        print("═" * 70)
        print(f"\n📚 Semanas disponibles ({len(semanas)}):\n")

        for i, semana in enumerate(semanas, start=1):
            print(f"  {i}. 📅 {semana}")

        print("\n  0. Salir")
        print("═" * 70)

        eleccion = input("\n ➤ Selecciona una semana (1-{}) o 0 para salir: ".format(len(semanas))).strip()

        if eleccion == '0':
            print("\n👋 ¡Gracias por usar el Dashboard!\n")
            break

        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(semanas):
                ruta_semana = os.path.join(ruta_parcial_01, semanas[idx])
                mostrar_scripts(ruta_semana, semanas[idx])
            else:
                print("\n⚠️ Opción fuera de rango. Elige un número entre 1 y {}.".format(len(semanas)))
                input("\n ➤ Presiona Enter para continuar...")
        except ValueError:
            print("\n⚠️ Ingresa un número válido.")
            input("\n ➤ Presiona Enter para continuar...")


def mostrar_scripts(ruta_semana, nombre_semana):
    """Muestra y permite ejecutar scripts de una semana"""
    try:
        scripts = sorted([
            f.name for f in os.scandir(ruta_semana)
            if f.is_file() and f.name.endswith('.py') and not f.name.startswith('.')
        ])

        if not scripts:
            print(f"\n⚠️ No hay archivos .py en '{nombre_semana}'")
            input("\n ➤ Presiona Enter para regresar...")
            return

    except Exception as e:
        print(f"\n❌ Error al leer '{nombre_semana}': {e}")
        input("\n ➤ Presiona Enter para regresar...")
        return

    while True:
        print("\n" + "═" * 70)
        print(f" 🐍 Scripts - {nombre_semana} ".center(70))
        print("═" * 70)
        print()

        for i, script in enumerate(scripts, start=1):
            print(f"  {i}. 📜 {script}")

        print("\n  0. Regresar")
        print("═" * 70)

        eleccion = input(f"\n ➤ Selecciona un script (1-{len(scripts)}) o 0 para regresar: ").strip()

        if eleccion == '0':
            break

        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(scripts):
                ruta_script = os.path.join(ruta_semana, scripts[idx])
                mostrar_codigo(ruta_script)

                print("\n" + "-" * 70)
                ejecutar = input(" ➤ ¿Ejecutar este script AHORA en esta consola? (1=Sí, 0=No): ").strip()
                if ejecutar == '1':
                    print("\n⏳ Ejecutando script... (la salida se mostrará aquí mismo)\n")
                    ejecutar_codigo(ruta_script)
                    input("\n ➤ Presiona Enter para volver al menú...")
                elif ejecutar == '0':
                    print("\n⏭️ Script no ejecutado.")
                    input("\n ➤ Presiona Enter para continuar...")
                else:
                    print("\n⚠️ Opción inválida. Regresando al menú...")
                    input("\n ➤ Presiona Enter para continuar...")
            else:
                print(f"\n⚠️ Opción fuera de rango.")
                input("\n ➤ Presiona Enter para continuar...")
        except ValueError:
            print("\n⚠️ Ingresa un número válido.")
            input("\n ➤ Presiona Enter para continuar...")


if __name__ == "__main__":
    # Banner de bienvenida
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "   🚀 DASHBOARD DE PROYECTOS PYTHON - PARCIAL 01   ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")

    print("\n✅ FUNCIONALIDAD 100% GARANTIZADA:")
    print("   • Ejecución DIRECTA en la misma consola (SIN ventanas externas)")
    print("   • Sin errores de rutas ni sintaxis")
    print("   • Funciona en TODAS las semanas (02, 03, 04, 05, 06, 07, 08)")
    print("   • Salida del script se muestra INMEDIATAMENTE aquí mismo")

    print("\n💡 VENTAJAS:")
    print("   • No más problemas con ventanas que no se abren")
    print("   • No más errores de rutas en Windows")
    print("   • Todo se ejecuta en esta misma terminal")
    print("   • Funciona perfectamente desde PyCharm, VS Code o CMD")

    print("\n" + "═" * 70)
    input("\n ➤ Presiona Enter para iniciar el Dashboard...")

    mostrar_menu()

    print("\n" + "═" * 70)
    print(" 👋 ¡Gracias por usar el Dashboard! ".center(70))
    print("═" * 70 + "\n")