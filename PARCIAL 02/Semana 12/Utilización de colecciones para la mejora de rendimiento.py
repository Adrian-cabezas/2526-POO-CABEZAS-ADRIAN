"""
=============================================================
  SISTEMA DE GESTION DE BIBLIOTECA DIGITAL
=============================================================
Autor: Sistema Biblioteca Digital
Descripcion: Sistema completo para gestionar libros, usuarios
             y prestamos en una biblioteca digital.
=============================================================
"""

from datetime import datetime

# ── Helpers de formato ────────────────────────────────────────
W  = 72          # ancho de línea
HL = "═" * W
HL2= "─" * W

def encabezado(texto: str) -> None:
    print(f"\n{HL}")
    print(f"  {texto}")
    print(HL)

def seccion(texto: str) -> None:
    relleno = max(0, W - len(texto) - 6)
    print(f"\n  ┌─ {texto} {'─' * relleno}┐")

def ok(msg: str)    -> None: print(f"  │  ✔  {msg}")
def aviso(msg: str) -> None: print(f"  │  ✘  {msg}")
def item(msg: str)  -> None: print(f"  │     {msg}")
def cerrar()        -> None: print(f"  └{'─' * (W - 2)}┘")


# -------------------------------------------------------------
#  CLASE: Libro
# -------------------------------------------------------------
class Libro:
    """
    Representa un libro de la biblioteca.

    Se utiliza una TUPLA para almacenar el autor y el titulo
    porque son atributos inmutables (no cambian una vez creados).
    """

    def __init__(self, titulo: str, autor: str, categoria: str, isbn: str):
        # Tupla inmutable: (titulo, autor) - no cambiara nunca
        self._info_inmutable = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn
        self.disponible = True  # True = disponible para prestamo

    @property
    def titulo(self) -> str:
        return self._info_inmutable[0]

    @property
    def autor(self) -> str:
        return self._info_inmutable[1]

    def estado_str(self) -> str:
        return "✔ Disponible" if self.disponible else "✘ Prestado  "

    def __str__(self) -> str:
        return (
            f"{self.estado_str()}  |  {self.titulo:<32}"
            f"  {self.autor:<25}  [{self.categoria}]"
        )

    def detalle(self) -> str:
        return (
            f"Titulo   : {self.titulo}\n"
            f"     Autor    : {self.autor}\n"
            f"     Categoria: {self.categoria}\n"
            f"     ISBN     : {self.isbn}\n"
            f"     Estado   : {self.estado_str()}"
        )

    def __repr__(self) -> str:
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}', isbn='{self.isbn}')"


# -------------------------------------------------------------
#  CLASE: Usuario
# -------------------------------------------------------------
class Usuario:
    """
    Representa a un usuario registrado en la biblioteca.

    Atributos:
        - nombre           : Nombre del usuario.
        - id_usuario       : Identificador unico (gestionado con SET en Biblioteca).
        - libros_prestados : LISTA de objetos Libro actualmente en prestamo.
    """

    def __init__(self, nombre: str, id_usuario: str):
        self.nombre = nombre
        self.id_usuario = id_usuario
        # Lista mutable: los libros prestados cambian con el tiempo
        self.libros_prestados: list[Libro] = []

    def __str__(self) -> str:
        cantidad = len(self.libros_prestados)
        barra = "█" * cantidad + "░" * (5 - min(cantidad, 5))
        return (
            f"[{self.id_usuario}]  {self.nombre:<20}"
            f"  Prestados: {cantidad}  {barra}"
        )

    def __repr__(self) -> str:
        return f"Usuario(nombre='{self.nombre}', id='{self.id_usuario}')"


# -------------------------------------------------------------
#  CLASE: Biblioteca
# -------------------------------------------------------------
class Biblioteca:
    """
    Clase principal que gestiona libros, usuarios y prestamos.

    Estructuras de datos utilizadas:
        - DICCIONARIO : almacena libros con ISBN como clave -> acceso O(1).
        - SET         : almacena IDs de usuario unicos -> sin duplicados.
        - DICCIONARIO : almacena usuarios con id_usuario como clave.
        - LISTA       : dentro de cada Usuario, lista de libros prestados.
    """

    def __init__(self, nombre: str):
        self.nombre = nombre
        self._libros: dict[str, Libro] = {}
        self._usuarios: dict[str, Usuario] = {}
        self._ids_usuarios: set[str] = set()
        self._historial: list[dict] = []

    # -- GESTION DE LIBROS -------------------------------------------

    def anadir_libro(self, libro: Libro) -> bool:
        if libro.isbn in self._libros:
            aviso(f"ISBN '{libro.isbn}' ya existe en el catalogo.")
            return False
        self._libros[libro.isbn] = libro
        ok(f"Añadido  →  {libro.titulo}  ({libro.autor})")
        return True

    def quitar_libro(self, isbn: str) -> bool:
        if isbn not in self._libros:
            aviso(f"No existe ningun libro con ISBN '{isbn}'.")
            return False
        libro = self._libros[isbn]
        if not libro.disponible:
            aviso(f"'{libro.titulo}' esta prestado y no puede eliminarse.")
            return False
        del self._libros[isbn]
        ok(f"Eliminado  →  '{libro.titulo}'  (ISBN: {isbn})")
        return True

    # -- GESTION DE USUARIOS -----------------------------------------

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if usuario.id_usuario in self._ids_usuarios:
            aviso(f"ID '{usuario.id_usuario}' ya esta en uso.")
            return False
        self._ids_usuarios.add(usuario.id_usuario)
        self._usuarios[usuario.id_usuario] = usuario
        ok(f"Registrado  →  {usuario.nombre}  (ID: {usuario.id_usuario})")
        return True

    def dar_de_baja_usuario(self, id_usuario: str) -> bool:
        if id_usuario not in self._usuarios:
            aviso(f"No existe usuario con ID '{id_usuario}'.")
            return False
        usuario = self._usuarios[id_usuario]
        if usuario.libros_prestados:
            titulos = ", ".join(f"'{l.titulo}'" for l in usuario.libros_prestados)
            aviso(f"{usuario.nombre} tiene libros sin devolver: {titulos}.")
            return False
        self._ids_usuarios.discard(id_usuario)
        del self._usuarios[id_usuario]
        ok(f"Dado de baja  →  {usuario.nombre}  (ID: {id_usuario})")
        return True

    # -- PRESTAMOS Y DEVOLUCIONES ------------------------------------

    def prestar_libro(self, id_usuario: str, isbn: str) -> bool:
        usuario = self._usuarios.get(id_usuario)
        libro   = self._libros.get(isbn)

        if not usuario:
            aviso(f"Usuario '{id_usuario}' no encontrado.")
            return False
        if not libro:
            aviso(f"Libro ISBN '{isbn}' no encontrado.")
            return False
        if not libro.disponible:
            aviso(f"'{libro.titulo}' no esta disponible para prestamo.")
            return False

        libro.disponible = False
        usuario.libros_prestados.append(libro)
        self._registrar_evento("PRESTAMO", usuario, libro)
        ok(f"Prestamo  →  '{libro.titulo}'  ──►  {usuario.nombre}")
        return True

    def devolver_libro(self, id_usuario: str, isbn: str) -> bool:
        usuario = self._usuarios.get(id_usuario)
        libro   = self._libros.get(isbn)

        if not usuario:
            aviso(f"Usuario '{id_usuario}' no encontrado.")
            return False
        if not libro:
            aviso(f"Libro ISBN '{isbn}' no encontrado.")
            return False
        if libro not in usuario.libros_prestados:
            aviso(f"{usuario.nombre} no tiene prestado '{libro.titulo}'.")
            return False

        # Realizar la devolucion
        libro.disponible = True
        usuario.libros_prestados.remove(libro)
        self._registrar_evento("DEVOLUCION", usuario, libro)
        ok(f"Devolucion  →  '{libro.titulo}'  ◄──  {usuario.nombre}")
        return True

    # -- BUSQUEDA DE LIBROS ------------------------------------------

    def buscar_por_titulo(self, titulo: str) -> list[Libro]:
        """Busca libros cuyo titulo contenga la cadena indicada."""
        resultados = [l for l in self._libros.values() if titulo.lower() in l.titulo.lower()]
        self._mostrar_resultados(resultados, f"Titulo contiene  '{titulo}'")
        return resultados

    def buscar_por_autor(self, autor: str) -> list[Libro]:
        """Busca libros por nombre de autor."""
        resultados = [l for l in self._libros.values() if autor.lower() in l.autor.lower()]
        self._mostrar_resultados(resultados, f"Autor contiene   '{autor}'")
        return resultados

    def buscar_por_categoria(self, categoria: str) -> list[Libro]:
        """Busca libros que pertenezcan a una categoria."""
        resultados = [l for l in self._libros.values() if categoria.lower() in l.categoria.lower()]
        self._mostrar_resultados(resultados, f"Categoria        '{categoria}'")
        return resultados

    # -- LISTADO DE LIBROS PRESTADOS ---------------------------------

    def listar_libros_prestados(self, id_usuario: str) -> list[Libro]:
        """Muestra todos los libros actualmente prestados a un usuario."""
        usuario = self._usuarios.get(id_usuario)
        if not usuario:
            aviso(f"Usuario con ID '{id_usuario}' no encontrado.")
            return []
        print(f"\n  ┌─ Prestados a: {usuario.nombre}  (ID: {usuario.id_usuario}) {'─'*(W-38)}┐")
        if not usuario.libros_prestados:
            item("(ninguno)")
        else:
            for i, libro in enumerate(usuario.libros_prestados, 1):
                item(f"{i}. {libro.titulo}  —  {libro.autor}  [{libro.categoria}]  ISBN:{libro.isbn}")
        cerrar()
        return usuario.libros_prestados

    # -- REPORTES Y UTILIDADES ---------------------------------------

    def mostrar_catalogo_completo(self) -> None:
        """Muestra todos los libros del catalogo con su estado actual."""
        encabezado(f"CATALOGO  ·  {self.nombre.upper()}")
        print(f"  {'ESTADO':<14}  {'TITULO':<30}  {'AUTOR':<22}  CATEGORIA")
        print("  " + "─" * (W - 2))
        if not self._libros:
            print("  El catalogo esta vacio.")
        else:
            for libro in self._libros.values():
                estado = "✔ Disponible" if libro.disponible else "✘ Prestado  "
                print(
                    f"  {estado:<14}  {libro.titulo:<30}  "
                    f"{libro.autor:<22}  {libro.categoria}"
                )
        print(HL + "\n")

    def mostrar_usuarios_registrados(self) -> None:
        """Muestra todos los usuarios registrados en el sistema."""
        encabezado(f"USUARIOS  ·  {self.nombre.upper()}")
        print(f"  {'ID':<6}  {'NOMBRE':<22}  {'PRESTADOS':<10}  ACTIVIDAD")
        print("  " + "─" * (W - 2))
        if not self._usuarios:
            print("  No hay usuarios registrados.")
        else:
            for u in self._usuarios.values():
                n = len(u.libros_prestados)
                barra = "█" * n + "░" * max(0, 5 - n)
                print(f"  {u.id_usuario:<6}  {u.nombre:<22}  {n:<10}  {barra}")
        print(HL + "\n")

    def mostrar_historial(self) -> None:
        """Muestra el historial de prestamos y devoluciones."""
        encabezado("HISTORIAL DE TRANSACCIONES")
        print(f"  {'#':<3}  {'HORA':<8}  {'TIPO':<12}  {'LIBRO':<28}  USUARIO")
        print("  " + "─" * (W - 2))
        if not self._historial:
            print("  Sin transacciones registradas.")
        else:
            for i, e in enumerate(self._historial, 1):
                hora = e['fecha'][11:]          # solo HH:MM:SS
                tipo = f"[{e['tipo']}]"
                icono = "▲" if e['tipo'] == "PRESTAMO" else "▼"
                print(
                    f"  {i:<3}  {hora:<8}  {icono} {tipo:<11}  "
                    f"{e['libro']:<28}  {e['usuario']}"
                )
        print(HL + "\n")

    # -- METODOS PRIVADOS --------------------------------------------

    def _registrar_evento(self, tipo: str, usuario: Usuario, libro: Libro) -> None:
        """Guarda un evento en el historial global."""
        self._historial.append({
            "tipo": tipo,
            "usuario": usuario.nombre,
            "libro": libro.titulo,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    def _mostrar_resultados(self, resultados: list[Libro], criterio: str) -> None:
        """Imprime los resultados de una busqueda de forma formateada."""
        n = len(resultados)
        print(f"\n  ┌─ Busqueda: {criterio}  —  {n} resultado/s {'─'*(W-40)}┐")
        if not resultados:
            item("Sin resultados.")
        else:
            for libro in resultados:
                item(f"{libro}")
        cerrar()


# -------------------------------------------------------------
#  DEMOSTRACION DEL SISTEMA
# -------------------------------------------------------------
def main():

    # ── PORTADA ────────────────────────────────────────────────
    print("\n" + HL)
    print(f"{'SISTEMA DE GESTION DE BIBLIOTECA DIGITAL':^{W}}")
    print(f"{'Biblioteca Central Digital':^{W}}")
    print(HL)

    biblioteca = Biblioteca("Biblioteca Central Digital")

    # ── 1. AÑADIR LIBROS ────────────────────────────────────────
    encabezado("1/8  AÑADIENDO LIBROS AL CATALOGO")
    seccion("Registrando 8 titulos...")
    libros = [
        Libro("Cien anos de soledad",         "Gabriel Garcia Marquez",   "Novela",           "978-0060883287"),
        Libro("El nombre de la rosa",          "Umberto Eco",              "Misterio",         "978-0156001311"),
        Libro("Sapiens",                       "Yuval Noah Harari",        "Historia",         "978-0062316097"),
        Libro("1984",                          "George Orwell",            "Distopia",         "978-0451524935"),
        Libro("El Quijote",                    "Miguel de Cervantes",      "Clasico",          "978-8467033793"),
        Libro("Dune",                          "Frank Herbert",            "Ciencia Ficcion",  "978-0441013593"),
        Libro("Brevisima historia del tiempo", "Stephen Hawking",          "Ciencia",          "978-8408060741"),
        Libro("El principito",                 "Antoine de Saint-Exupery", "Infantil",         "978-0156012195"),
    ]
    for libro in libros:
        biblioteca.anadir_libro(libro)
    cerrar()

    # ── 2. REGISTRAR USUARIOS ───────────────────────────────────
    encabezado("2/8  REGISTRANDO USUARIOS")
    seccion("Registrando 4 usuarios...")
    usuarios = [
        Usuario("Lucia Martinez", "U001"),
        Usuario("Carlos Perez",   "U002"),
        Usuario("Ana Garcia",     "U003"),
        Usuario("Miguel Lopez",   "U004"),
    ]
    for usuario in usuarios:
        biblioteca.registrar_usuario(usuario)
    cerrar()

    # ── 3. PRUEBA: ID DUPLICADO ─────────────────────────────────
    encabezado("3/8  PRUEBA — REGISTRO CON ID DUPLICADO")
    seccion("Intentando registrar ID ya existente (U001)...")
    biblioteca.registrar_usuario(Usuario("Impostora", "U001"))
    cerrar()

    # ── 4. CATALOGO INICIAL ─────────────────────────────────────
    biblioteca.mostrar_catalogo_completo()

    # ── 5. PRESTAMOS ────────────────────────────────────────────
    encabezado("4/8  REALIZANDO PRESTAMOS")
    seccion("5 prestamos en curso...")
    biblioteca.prestar_libro("U001", "978-0060883287")
    biblioteca.prestar_libro("U001", "978-0062316097")
    biblioteca.prestar_libro("U002", "978-0451524935")
    biblioteca.prestar_libro("U003", "978-0156001311")
    biblioteca.prestar_libro("U004", "978-0441013593")
    cerrar()

    encabezado("  PRUEBA — PRESTAR LIBRO NO DISPONIBLE")
    seccion("Intentando prestar 'Cien anos' (ya prestado a Lucia)...")
    biblioteca.prestar_libro("U002", "978-0060883287")
    cerrar()

    # ── 6. LIBROS PRESTADOS POR USUARIO ─────────────────────────
    encabezado("5/8  LIBROS PRESTADOS POR USUARIO")
    for u in usuarios:
        biblioteca.listar_libros_prestados(u.id_usuario)

    # ── 7. BUSQUEDAS ────────────────────────────────────────────
    encabezado("6/8  BUSQUEDAS EN EL CATALOGO")
    biblioteca.buscar_por_titulo("1984")
    biblioteca.buscar_por_autor("Harari")
    biblioteca.buscar_por_categoria("Ciencia")

    # ── 8. DEVOLUCIONES ─────────────────────────────────────────
    encabezado("7/8  DEVOLUCIONES")
    seccion("Lucia y Carlos devuelven sus libros...")
    biblioteca.devolver_libro("U001", "978-0060883287")
    biblioteca.devolver_libro("U002", "978-0451524935")
    cerrar()

    encabezado("  PRUEBA — BAJA CON LIBROS PENDIENTES")
    seccion("Lucia aun tiene 'Sapiens'...")
    biblioteca.dar_de_baja_usuario("U001")
    cerrar()

    encabezado("  LUCIA DEVUELVE SAPIENS Y SE DA DE BAJA")
    seccion("Devolucion y baja definitiva...")
    biblioteca.devolver_libro("U001", "978-0062316097")
    biblioteca.dar_de_baja_usuario("U001")
    cerrar()

    encabezado("  QUITAR LIBRO DEL CATALOGO")
    seccion("Eliminando 'El principito' (disponible) e intentando eliminar uno prestado...")
    biblioteca.quitar_libro("978-0156012195")
    biblioteca.quitar_libro("978-0156001311")
    cerrar()

    # ── 9. ESTADO FINAL ─────────────────────────────────────────
    encabezado("8/8  ESTADO FINAL DEL SISTEMA")
    biblioteca.mostrar_catalogo_completo()
    biblioteca.mostrar_usuarios_registrados()
    biblioteca.mostrar_historial()

    # ── CIERRE ──────────────────────────────────────────────────
    print(HL)
    print(f"{'DEMOSTRACION COMPLETADA EXITOSAMENTE':^{W}}")
    print(HL + "\n")

    return biblioteca


# -------------------------------------------------------------
#  MENU INTERACTIVO
# -------------------------------------------------------------
def menu_interactivo(biblioteca: Biblioteca) -> None:
    """
    Menu principal que permite al usuario ejecutar todas las
    funcionalidades del sistema de forma interactiva.
    """

    opciones = {
        "1": "Añadir libro",
        "2": "Quitar libro",
        "3": "Registrar usuario",
        "4": "Dar de baja usuario",
        "5": "Prestar libro",
        "6": "Devolver libro",
        "7": "Buscar libros",
        "8": "Listar libros prestados de un usuario",
        "9": "Ver catalogo completo",
        "10": "Ver usuarios registrados",
        "11": "Ver historial de transacciones",
        "0": "Salir",
    }

    while True:
        print(f"\n{HL}")
        print(f"{'MENU PRINCIPAL':^{W}}")
        print(HL)
        for clave, desc in opciones.items():
            print(f"  [{clave:>2}]  {desc}")
        print(HL)

        opcion = input("\n  Elige una opcion: ").strip()

        # ── 1. AÑADIR LIBRO ──────────────────────────────────────
        if opcion == "1":
            encabezado("AÑADIR LIBRO")
            titulo    = input("  Titulo    : ").strip()
            autor     = input("  Autor     : ").strip()
            categoria = input("  Categoria : ").strip()
            isbn      = input("  ISBN      : ").strip()
            if titulo and autor and categoria and isbn:
                seccion("Procesando...")
                biblioteca.anadir_libro(Libro(titulo, autor, categoria, isbn))
                cerrar()
            else:
                print("  ✘  Todos los campos son obligatorios.")

        # ── 2. QUITAR LIBRO ──────────────────────────────────────
        elif opcion == "2":
            encabezado("QUITAR LIBRO")
            isbn = input("  ISBN del libro a eliminar: ").strip()
            seccion("Procesando...")
            biblioteca.quitar_libro(isbn)
            cerrar()

        # ── 3. REGISTRAR USUARIO ─────────────────────────────────
        elif opcion == "3":
            encabezado("REGISTRAR USUARIO")
            nombre = input("  Nombre      : ").strip()
            uid    = input("  ID usuario  : ").strip()
            if nombre and uid:
                seccion("Procesando...")
                biblioteca.registrar_usuario(Usuario(nombre, uid))
                cerrar()
            else:
                print("  ✘  Nombre e ID son obligatorios.")

        # ── 4. DAR DE BAJA USUARIO ───────────────────────────────
        elif opcion == "4":
            encabezado("DAR DE BAJA USUARIO")
            uid = input("  ID del usuario a dar de baja: ").strip()
            seccion("Procesando...")
            biblioteca.dar_de_baja_usuario(uid)
            cerrar()

        # ── 5. PRESTAR LIBRO ─────────────────────────────────────
        elif opcion == "5":
            encabezado("PRESTAR LIBRO")
            uid  = input("  ID del usuario  : ").strip()
            isbn = input("  ISBN del libro  : ").strip()
            seccion("Procesando...")
            biblioteca.prestar_libro(uid, isbn)
            cerrar()

        # ── 6. DEVOLVER LIBRO ────────────────────────────────────
        elif opcion == "6":
            encabezado("DEVOLVER LIBRO")
            uid  = input("  ID del usuario  : ").strip()
            isbn = input("  ISBN del libro  : ").strip()
            seccion("Procesando...")
            biblioteca.devolver_libro(uid, isbn)
            cerrar()

        # ── 7. BUSCAR LIBROS ─────────────────────────────────────
        elif opcion == "7":
            encabezado("BUSCAR LIBROS")
            print("  [1] Por titulo")
            print("  [2] Por autor")
            print("  [3] Por categoria")
            sub = input("\n  Tipo de busqueda: ").strip()
            if sub == "1":
                termino = input("  Titulo (o parte): ").strip()
                biblioteca.buscar_por_titulo(termino)
            elif sub == "2":
                termino = input("  Autor (o parte): ").strip()
                biblioteca.buscar_por_autor(termino)
            elif sub == "3":
                termino = input("  Categoria: ").strip()
                biblioteca.buscar_por_categoria(termino)
            else:
                print("  ✘  Opcion no valida.")

        # ── 8. LISTAR LIBROS PRESTADOS ───────────────────────────
        elif opcion == "8":
            encabezado("LIBROS PRESTADOS POR USUARIO")
            uid = input("  ID del usuario: ").strip()
            biblioteca.listar_libros_prestados(uid)

        # ── 9. CATALOGO COMPLETO ─────────────────────────────────
        elif opcion == "9":
            biblioteca.mostrar_catalogo_completo()

        # ── 10. USUARIOS REGISTRADOS ─────────────────────────────
        elif opcion == "10":
            biblioteca.mostrar_usuarios_registrados()

        # ── 11. HISTORIAL ────────────────────────────────────────
        elif opcion == "11":
            biblioteca.mostrar_historial()

        # ── 0. SALIR ─────────────────────────────────────────────
        elif opcion == "0":
            print(f"\n{HL}")
            print(f"{'Hasta pronto. Sesion cerrada.':^{W}}")
            print(HL + "\n")
            break

        else:
            print("  ✘  Opcion no reconocida. Elige entre 0 y 11.")


if __name__ == "__main__":
    # Primero corre la demo automatica con datos de ejemplo
    biblioteca = main()

    # Luego abre el menu interactivo sobre la misma biblioteca
    print(f"\n{HL}")
    print(f"{'INICIANDO MODO INTERACTIVO':^{W}}")
    print(f"{'Puedes operar sobre los datos cargados en la demo':^{W}}")
    print(HL)
    menu_interactivo(biblioteca)