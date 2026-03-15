"""
Aplicación GUI Básica - Gestión de Tareas
==========================================
Autor: Actividad académica
Descripción:
    Aplicación de interfaz gráfica que permite al usuario agregar, visualizar
    y eliminar tareas mediante componentes GUI: etiquetas, botones, campos de
    texto y una tabla (Treeview).

Librería utilizada: Tkinter (incluida en la biblioteca estándar de Python).
"""

import tkinter as tk
from tkinter import ttk, messagebox


# ─────────────────────────────────────────────
#  Lógica / Funciones de la aplicación
# ─────────────────────────────────────────────

def agregar_tarea():
    """
    Lee el contenido del campo de texto y lo inserta en la tabla.
    Muestra una advertencia si el campo está vacío.
    """
    tarea = entrada_tarea.get().strip()
    categoria = combo_categoria.get()

    if not tarea:
        messagebox.showwarning("Campo vacío", "Por favor escribe una tarea antes de agregar.")
        return

    # Insertar fila en el Treeview con un ID autoincremental
    nuevo_id = len(tabla.get_children()) + 1
    tabla.insert("", tk.END, values=(nuevo_id, tarea, categoria, "Pendiente"))

    # Limpiar el campo de texto después de agregar
    entrada_tarea.delete(0, tk.END)
    entrada_tarea.focus()

    actualizar_contador()


def limpiar():
    """
    Botón 'Limpiar':
    - Borra siempre el texto escrito en el campo de entrada.
    - Si hay filas seleccionadas en la tabla, las elimina también.
    Cumple el requisito: 'borre la información ingresada o seleccionada por el usuario'.
    """
    # 1. Limpiar siempre el campo de texto
    entrada_tarea.delete(0, tk.END)
    entrada_tarea.focus()

    # 2. Si hay filas seleccionadas en la tabla, eliminarlas
    seleccionados = tabla.selection()
    if seleccionados:
        for item in seleccionados:
            tabla.delete(item)
        actualizar_contador()


def limpiar_todo():
    """
    Elimina TODAS las tareas de la tabla tras pedir confirmación.
    """
    if not tabla.get_children():
        messagebox.showinfo("Sin tareas", "La lista ya está vacía.")
        return

    confirmacion = messagebox.askyesno(
        "Limpiar todo",
        "¿Estás seguro de que deseas eliminar TODAS las tareas?"
    )
    if confirmacion:
        for item in tabla.get_children():
            tabla.delete(item)
        entrada_tarea.delete(0, tk.END)
        actualizar_contador()


def marcar_completada():
    """
    Cambia el estado de la tarea seleccionada a 'Completada'.
    """
    seleccionados = tabla.selection()
    if not seleccionados:
        messagebox.showinfo("Sin selección", "Selecciona una tarea para marcarla como completada.")
        return

    for item in seleccionados:
        valores = list(tabla.item(item, "values"))
        valores[3] = "✔ Completada"
        tabla.item(item, values=valores)
        tabla.tag_configure("completada", foreground="#27ae60")
        tabla.item(item, tags=("completada",))


def actualizar_contador():
    """Actualiza la etiqueta que muestra el total de tareas registradas."""
    total = len(tabla.get_children())
    lbl_contador.config(text=f"Total de tareas: {total}")


def on_enter_key(event):
    """Permite agregar una tarea presionando la tecla Enter."""
    agregar_tarea()


# ─────────────────────────────────────────────
#  Construcción de la ventana principal
# ─────────────────────────────────────────────

# Ventana raíz
ventana = tk.Tk()
ventana.title("Gestor de Tareas — Aplicación GUI")
ventana.geometry("780x560")
ventana.resizable(True, True)
ventana.configure(bg="#f0f4f8")

# ── Estilo ttk ──────────────────────────────
estilo = ttk.Style()
estilo.theme_use("clam")

estilo.configure("Treeview",
                 background="#ffffff",
                 foreground="#2d3436",
                 rowheight=28,
                 fieldbackground="#ffffff",
                 font=("Segoe UI", 10))

estilo.configure("Treeview.Heading",
                 background="#2c3e50",
                 foreground="#ffffff",
                 font=("Segoe UI", 10, "bold"))

estilo.map("Treeview", background=[("selected", "#3498db")])

estilo.configure("TCombobox", font=("Segoe UI", 10))


# ─────────────────────────────────────────────
#  SECCIÓN 1 — Encabezado
# ─────────────────────────────────────────────

frame_header = tk.Frame(ventana, bg="#2c3e50", pady=14)
frame_header.pack(fill=tk.X)

lbl_titulo = tk.Label(
    frame_header,
    text="📋  Gestor de Tareas",
    font=("Segoe UI", 18, "bold"),
    bg="#2c3e50",
    fg="#ecf0f1"
)
lbl_titulo.pack()

lbl_subtitulo = tk.Label(
    frame_header,
    text="Organiza tus actividades de forma sencilla",
    font=("Segoe UI", 10),
    bg="#2c3e50",
    fg="#bdc3c7"
)
lbl_subtitulo.pack()


# ─────────────────────────────────────────────
#  SECCIÓN 2 — Formulario de entrada
# ─────────────────────────────────────────────

frame_form = tk.LabelFrame(
    ventana,
    text=" Nueva Tarea ",
    font=("Segoe UI", 10, "bold"),
    bg="#f0f4f8",
    fg="#2c3e50",
    padx=14,
    pady=10
)
frame_form.pack(fill=tk.X, padx=20, pady=(14, 6))

# Etiqueta + campo de texto
lbl_tarea = tk.Label(frame_form, text="Descripción:", font=("Segoe UI", 10), bg="#f0f4f8", fg="#2c3e50")
lbl_tarea.grid(row=0, column=0, sticky=tk.W, padx=(0, 8))

entrada_tarea = tk.Entry(frame_form, font=("Segoe UI", 11), width=38, relief=tk.FLAT,
                         highlightthickness=1, highlightbackground="#bdc3c7",
                         highlightcolor="#3498db")
entrada_tarea.grid(row=0, column=1, padx=(0, 12), ipady=5)
entrada_tarea.bind("<Return>", on_enter_key)  # Evento tecla Enter
entrada_tarea.focus()

# Etiqueta + combo de categoría
lbl_cat = tk.Label(frame_form, text="Categoría:", font=("Segoe UI", 10), bg="#f0f4f8", fg="#2c3e50")
lbl_cat.grid(row=0, column=2, sticky=tk.W, padx=(0, 8))

combo_categoria = ttk.Combobox(
    frame_form,
    values=["General", "Trabajo", "Estudio", "Personal", "Urgente"],
    state="readonly",
    width=14,
    font=("Segoe UI", 10)
)
combo_categoria.current(0)
combo_categoria.grid(row=0, column=3, padx=(0, 12))

# Botón Agregar
btn_agregar = tk.Button(
    frame_form,
    text="➕  Agregar",
    command=agregar_tarea,
    font=("Segoe UI", 10, "bold"),
    bg="#27ae60",
    fg="#ffffff",
    activebackground="#219a52",
    activeforeground="#ffffff",
    relief=tk.FLAT,
    padx=12,
    pady=5,
    cursor="hand2"
)
btn_agregar.grid(row=0, column=4, padx=(0, 6))

# Botón Limpiar — borra el campo de texto y/o la selección de la tabla
btn_limpiar_form = tk.Button(
    frame_form,
    text="🧹  Limpiar",
    command=limpiar,
    font=("Segoe UI", 10, "bold"),
    bg="#e67e22",
    fg="#ffffff",
    activebackground="#ca6f1e",
    activeforeground="#ffffff",
    relief=tk.FLAT,
    padx=12,
    pady=5,
    cursor="hand2"
)
btn_limpiar_form.grid(row=0, column=5)


# ─────────────────────────────────────────────
#  SECCIÓN 3 — Tabla de tareas (Treeview)
# ─────────────────────────────────────────────

frame_tabla = tk.LabelFrame(
    ventana,
    text=" Lista de Tareas ",
    font=("Segoe UI", 10, "bold"),
    bg="#f0f4f8",
    fg="#2c3e50",
    padx=14,
    pady=10
)
frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=6)

# Scrollbar vertical
scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Treeview (tabla)
columnas = ("id", "tarea", "categoria", "estado")
tabla = ttk.Treeview(
    frame_tabla,
    columns=columnas,
    show="headings",
    yscrollcommand=scrollbar.set,
    selectmode="extended"   # permite selección múltiple con Ctrl/Shift
)
scrollbar.config(command=tabla.yview)

# Configuración de columnas
tabla.heading("id",        text="#",          anchor=tk.CENTER)
tabla.heading("tarea",     text="Descripción",anchor=tk.W)
tabla.heading("categoria", text="Categoría",  anchor=tk.CENTER)
tabla.heading("estado",    text="Estado",     anchor=tk.CENTER)

tabla.column("id",        width=40,  anchor=tk.CENTER, stretch=False)
tabla.column("tarea",     width=380, anchor=tk.W)
tabla.column("categoria", width=120, anchor=tk.CENTER, stretch=False)
tabla.column("estado",    width=130, anchor=tk.CENTER, stretch=False)

tabla.pack(fill=tk.BOTH, expand=True)

# Filas alternas (zebra stripes)
tabla.tag_configure("par",   background="#f8f9fa")
tabla.tag_configure("impar", background="#ffffff")


# ─────────────────────────────────────────────
#  SECCIÓN 4 — Barra de acciones inferiores
# ─────────────────────────────────────────────

frame_acciones = tk.Frame(ventana, bg="#f0f4f8", pady=8)
frame_acciones.pack(fill=tk.X, padx=20)

# Contador de tareas (izquierda)
lbl_contador = tk.Label(
    frame_acciones,
    text="Total de tareas: 0",
    font=("Segoe UI", 10),
    bg="#f0f4f8",
    fg="#7f8c8d"
)
lbl_contador.pack(side=tk.LEFT)

# Botones de acción (derecha)
btn_completar = tk.Button(
    frame_acciones,
    text="✔  Completada",
    command=marcar_completada,
    font=("Segoe UI", 10),
    bg="#3498db",
    fg="#ffffff",
    activebackground="#2980b9",
    activeforeground="#ffffff",
    relief=tk.FLAT,
    padx=10,
    pady=4,
    cursor="hand2"
)
btn_completar.pack(side=tk.RIGHT, padx=(6, 0))

btn_limpiar_todo = tk.Button(
    frame_acciones,
    text="🗑  Limpiar Todo",
    command=limpiar_todo,
    font=("Segoe UI", 10),
    bg="#e74c3c",
    fg="#ffffff",
    activebackground="#c0392b",
    activeforeground="#ffffff",
    relief=tk.FLAT,
    padx=10,
    pady=4,
    cursor="hand2"
)
btn_limpiar_todo.pack(side=tk.RIGHT, padx=(6, 0))

btn_limpiar = tk.Button(
    frame_acciones,
    text="Limpiar",
    command=limpiar,
    font=("Segoe UI", 10),
    bg="#e67e22",
    fg="#ffffff",
    activebackground="#ca6f1e",
    activeforeground="#ffffff",
    relief=tk.FLAT,
    padx=10,
    pady=4,
    cursor="hand2"
)
btn_limpiar.pack(side=tk.RIGHT, padx=(6, 0))


# ─────────────────────────────────────────────
#  Pie de página
# ─────────────────────────────────────────────

frame_footer = tk.Frame(ventana, bg="#dfe6e9", pady=4)
frame_footer.pack(fill=tk.X, side=tk.BOTTOM)

lbl_footer = tk.Label(
    frame_footer,
    text="Aplicación GUI con Tkinter  |  Python  |  Actividad académica",
    font=("Segoe UI", 8),
    bg="#dfe6e9",
    fg="#7f8c8d"
)
lbl_footer.pack()


# ─────────────────────────────────────────────
#  Iniciar el bucle principal de eventos
# ─────────────────────────────────────────────

ventana.mainloop()