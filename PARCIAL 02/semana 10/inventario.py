from producto import Producto
from typing import List
import os

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES DE CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────────────────────
ARCHIVO_INVENTARIO = "inventario.txt"  # Ruta del archivo de persistencia
SEPARADOR = "|"                        # Delimitador de campos en cada línea


class Inventario:
    """
    Gestiona la colección de productos de la tienda.

    MEJORAS v2:
    - Persistencia automática: cada cambio (agregar, eliminar, actualizar)
      se escribe de inmediato en ARCHIVO_INVENTARIO.
    - Recuperación automática: al instanciar, lee el archivo y reconstruye
      el inventario en memoria.
    - Manejo de excepciones: captura FileNotFoundError, PermissionError y
      errores de formato (líneas corruptas) de forma explícita y controlada.
    - Notificaciones: informa al usuario del éxito o fallo de cada operación
      de archivo mediante mensajes claros en consola.
    """

    def __init__(self):
        self._productos: List[Producto] = []
        self._indice_por_id: dict[int, Producto] = {}  # Acceso O(1) por ID

        # Al crear el inventario cargamos los datos persistidos (si existen)
        self._cargar_desde_archivo()

    # ─────────────────────────────────────────────────────────────────────────
    # MÉTODOS PRIVADOS DE PERSISTENCIA
    # ─────────────────────────────────────────────────────────────────────────

    def _guardar_en_archivo(self) -> None:
        """
        Serializa el inventario completo y lo escribe en ARCHIVO_INVENTARIO.

        Formato de cada línea:
            id|nombre|cantidad|precio

        Excepciones manejadas:
            - PermissionError : no tenemos permisos de escritura → aviso al usuario.
            - OSError         : otros errores de I/O (disco lleno, ruta inválida…).
        """
        try:
            # Abrimos en modo escritura ('w') para sobreescribir todo el archivo.
            # Esto garantiza que el archivo siempre refleje el estado actual exacto.
            with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo:
                for producto in self._productos:
                    # Construimos la línea con el separador elegido
                    linea = (f"{producto.id}{SEPARADOR}"
                             f"{producto.nombre}{SEPARADOR}"
                             f"{producto.cantidad}{SEPARADOR}"
                             f"{producto.precio}\n")
                    archivo.write(linea)

        except PermissionError:
            # El sistema operativo denegó el acceso de escritura al archivo
            print(f"[ERROR] Sin permisos de escritura en '{ARCHIVO_INVENTARIO}'. "
                  "El cambio se aplicó en memoria pero NO se guardó en disco.")

        except OSError as e:
            # Captura genérica para otros errores de E/S no contemplados antes
            print(f"[ERROR] Fallo al guardar el inventario en disco: {e}")

    def _cargar_desde_archivo(self) -> None:
        """
        Lee ARCHIVO_INVENTARIO y reconstruye el inventario en memoria.

        Flujo de carga:
            1. Intentamos abrir el archivo directamente.
            2. Si no existe (FileNotFoundError), lo creamos vacío y continuamos.
            3. Si no tenemos permisos (PermissionError), avisamos y arrancamos vacíos.
            4. Por cada línea válida creamos un Producto y lo indexamos.
            5. Las líneas corruptas se saltan con un aviso sin detener el programa.

        Excepciones manejadas:
            - FileNotFoundError : archivo ausente → se crea uno nuevo vacío.
            - PermissionError   : sin permiso de lectura → inventario vacío.
            - OSError           : otros errores de I/O.
        """
        try:
            # Intentamos abrir directamente; si no existe Python lanzará FileNotFoundError
            with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()

        except FileNotFoundError:
            # Primera ejecución o archivo borrado externamente: creamos uno vacío
            print(f"[INFO] Archivo '{ARCHIVO_INVENTARIO}' no encontrado. "
                  "Se creará automáticamente al agregar el primer producto.")
            self._crear_archivo_vacio()
            return  # No hay datos que cargar; salimos

        except PermissionError:
            # No podemos leer el archivo → arrancamos con inventario vacío
            print(f"[ERROR] Sin permisos de lectura en '{ARCHIVO_INVENTARIO}'. "
                  "El inventario iniciará vacío en esta sesión.")
            return

        except OSError as e:
            print(f"[ERROR] No se pudo leer el archivo de inventario: {e}")
            return

        # ── Procesamiento línea por línea ──────────────────────────────────
        productos_cargados = 0

        for num_linea, linea in enumerate(lineas, start=1):
            linea = linea.strip()

            # Ignorar líneas vacías (pueden existir al final del archivo)
            if not linea:
                continue

            partes = linea.split(SEPARADOR)

            # Validamos que la línea tenga exactamente 4 campos
            if len(partes) != 4:
                print(f"[ADVERTENCIA] Línea {num_linea} con formato incorrecto "
                      f"(ignorada): '{linea}'")
                continue

            try:
                # Convertimos cada campo al tipo esperado
                id_prod  = int(partes[0])
                nombre   = partes[1]
                cantidad = int(partes[2])
                precio   = float(partes[3])

                # Creamos el Producto (puede lanzar ValueError si los valores son inválidos)
                producto = Producto(id_prod, nombre, cantidad, precio)

                # Evitamos cargar IDs duplicados que puedan existir en el archivo
                if producto.id in self._indice_por_id:
                    print(f"[ADVERTENCIA] ID duplicado en línea {num_linea} "
                          f"(ignorado): ID {id_prod}")
                    continue

                # Registro directo sin mensajes de "producto agregado"
                # para no saturar la consola al arrancar
                self._productos.append(producto)
                self._indice_por_id[producto.id] = producto
                productos_cargados += 1

            except ValueError as e:
                # Línea con datos no convertibles o que violan validaciones de Producto
                print(f"[ADVERTENCIA] Línea {num_linea} contiene datos inválidos "
                      f"(ignorada): {e}")

        # ── Resumen de carga ───────────────────────────────────────────────
        if productos_cargados > 0:
            print(f"[INFO] {productos_cargados} producto(s) cargado(s) "
                  f"exitosamente desde '{ARCHIVO_INVENTARIO}'.")
        else:
            print(f"[INFO] El archivo '{ARCHIVO_INVENTARIO}' existe pero no "
                  "contiene productos válidos. El inventario iniciará vacío.")

    def _crear_archivo_vacio(self) -> None:
        """
        Crea ARCHIVO_INVENTARIO vacío para que futuras escrituras funcionen.

        Excepciones manejadas:
            - PermissionError : no podemos crear el archivo en esta ruta.
            - OSError         : otros errores de E/S.
        """
        try:
            with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8"):
                pass  # Solo necesitamos que el archivo quede creado y vacío
            print(f"[INFO] Archivo '{ARCHIVO_INVENTARIO}' creado correctamente.")

        except PermissionError:
            print(f"[ERROR] Sin permisos para crear '{ARCHIVO_INVENTARIO}'. "
                  "Los datos no se persistirán durante esta sesión.")

        except OSError as e:
            print(f"[ERROR] No se pudo crear el archivo de inventario: {e}")

    # ─────────────────────────────────────────────────────────────────────────
    # MÉTODOS PÚBLICOS DE GESTIÓN
    # ─────────────────────────────────────────────────────────────────────────

    def agregar_producto(self, producto: Producto) -> bool:
        """
        Añade un producto al inventario si su ID no existe ya.
        Persiste el cambio en archivo y notifica al usuario.
        """
        if producto.id in self._indice_por_id:
            print(f"[ERROR] Ya existe un producto con ID {producto.id}. "
                  "No se realizó ningún cambio.")
            return False

        # Agregamos en memoria
        self._productos.append(producto)
        self._indice_por_id[producto.id] = producto

        # Persistimos inmediatamente en disco
        self._guardar_en_archivo()

        # Notificamos éxito al usuario
        print(f"[OK] Producto '{producto.nombre}' (ID: {producto.id}) agregado "
              f"exitosamente y guardado en '{ARCHIVO_INVENTARIO}'.")
        return True

    def eliminar_producto(self, id_producto: int) -> bool:
        """
        Elimina un producto por su ID.
        Persiste el inventario actualizado en archivo y notifica al usuario.
        """
        if id_producto not in self._indice_por_id:
            print(f"[ERROR] No se encontró ningún producto con ID {id_producto}.")
            return False

        # Eliminamos de ambas estructuras de datos
        producto = self._indice_por_id.pop(id_producto)
        self._productos.remove(producto)

        # Persistimos el estado actualizado
        self._guardar_en_archivo()

        print(f"[OK] Producto '{producto.nombre}' (ID: {id_producto}) eliminado "
              f"y cambios guardados en '{ARCHIVO_INVENTARIO}'.")
        return True

    def actualizar_cantidad(self, id_producto: int, nueva_cantidad: int) -> bool:
        """
        Actualiza solo la cantidad de stock de un producto.
        Persiste el cambio en archivo y notifica al usuario.
        """
        producto = self._indice_por_id.get(id_producto)
        if producto is None:
            print(f"[ERROR] No se encontró ningún producto con ID {id_producto}.")
            return False

        try:
            producto.cantidad = nueva_cantidad

            # Guardamos el cambio inmediatamente
            self._guardar_en_archivo()

            print(f"[OK] Cantidad actualizada → {producto}")
            print(f"     Cambio guardado exitosamente en '{ARCHIVO_INVENTARIO}'.")
            return True

        except ValueError as e:
            # La clase Producto lanza ValueError si la cantidad es negativa
            print(f"[ERROR] Valor inválido para cantidad: {e}")
            return False

    def actualizar_precio(self, id_producto: int, nuevo_precio: float) -> bool:
        """
        Actualiza solo el precio unitario de un producto.
        Persiste el cambio en archivo y notifica al usuario.
        """
        producto = self._indice_por_id.get(id_producto)
        if producto is None:
            print(f"[ERROR] No se encontró ningún producto con ID {id_producto}.")
            return False

        try:
            producto.precio = nuevo_precio

            # Guardamos el cambio inmediatamente
            self._guardar_en_archivo()

            print(f"[OK] Precio actualizado → {producto}")
            print(f"     Cambio guardado exitosamente en '{ARCHIVO_INVENTARIO}'.")
            return True

        except ValueError as e:
            # La clase Producto lanza ValueError si el precio es negativo
            print(f"[ERROR] Valor inválido para precio: {e}")
            return False

    def buscar_por_nombre(self, texto: str) -> List[Producto]:
        """Búsqueda parcial por nombre (insensible a mayúsculas/minúsculas)."""
        texto = texto.lower().strip()
        return [p for p in self._productos if texto in p.nombre.lower()]

    def mostrar_todos(self) -> None:
        """Muestra todos los productos en consola, ordenados por nombre."""
        if not self._productos:
            print("El inventario está vacío.")
            return

        print("\n" + "═" * 70)
        print(f"{'ID':4}  {'Nombre':25}  {'Cant.':6}  {'Precio':8}")
        print("─" * 70)

        for producto in sorted(self._productos, key=lambda p: p.nombre):
            print(producto)

        print("═" * 70)

    def contar_productos(self) -> int:
        """Retorna el número total de productos en el inventario."""
        return len(self._productos)