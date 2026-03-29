"""
Aplicación GUI de Lista de Tareas
Desarrollada con Tkinter para gestionar tareas: añadir, marcar como completada y eliminar.
"""

import tkinter as tk
from tkinter import messagebox


class TodoApp:
    """Clase principal de la aplicación de Lista de Tareas."""

    def __init__(self, root):
        """
        Inicializa la aplicación con la ventana principal.

        Args:
            root: La ventana raíz de Tkinter.
        """
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("550x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        # Lista interna para rastrear el estado de cada tarea
        self.tasks = []  # Cada elemento: {"text": str, "completed": bool}

        self._build_ui()

    # ──────────────────────────────────────────────
    # Construcción de la interfaz
    # ──────────────────────────────────────────────

    def _build_ui(self):
        """Construye todos los widgets de la interfaz gráfica."""

        # ── Título ──
        title_label = tk.Label(
            self.root,
            text="📝 Lista de Tareas",
            font=("Helvetica", 18, "bold"),
            bg="#f0f4f8",
            fg="#2d3748"
        )
        title_label.pack(pady=(18, 8))

        # ── Frame de entrada ──
        input_frame = tk.Frame(self.root, bg="#f0f4f8")
        input_frame.pack(padx=20, pady=6, fill="x")

        self.task_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 13),
            relief="flat",
            bg="#ffffff",
            fg="#2d3748",
            insertbackground="#2d3748",
            bd=2,
            highlightthickness=1,
            highlightbackground="#cbd5e0",
            highlightcolor="#4299e1"
        )
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        # Permitir añadir tarea presionando Enter
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        add_btn = tk.Button(
            input_frame,
            text="➕ Añadir",
            font=("Helvetica", 11, "bold"),
            bg="#4299e1",
            fg="white",
            activebackground="#2b6cb0",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.add_task
        )
        add_btn.pack(side="right")

        # ── Frame de la lista ──
        list_frame = tk.Frame(self.root, bg="#f0f4f8")
        list_frame.pack(padx=20, pady=6, fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Helvetica", 12),
            selectbackground="#bee3f8",
            selectforeground="#2d3748",
            bg="#ffffff",
            fg="#2d3748",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground="#cbd5e0",
            activestyle="none",
            yscrollcommand=scrollbar.set
        )
        self.task_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        # Doble clic para marcar/desmarcar completada
        self.task_listbox.bind("<Double-Button-1>", lambda event: self.toggle_complete())

        # ── Frame de botones de acción ──
        btn_frame = tk.Frame(self.root, bg="#f0f4f8")
        btn_frame.pack(padx=20, pady=10, fill="x")

        complete_btn = tk.Button(
            btn_frame,
            text="✔ Marcar como Completada",
            font=("Helvetica", 11),
            bg="#48bb78",
            fg="white",
            activebackground="#276749",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.toggle_complete
        )
        complete_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))

        delete_btn = tk.Button(
            btn_frame,
            text="🗑 Eliminar Tarea",
            font=("Helvetica", 11),
            bg="#fc8181",
            fg="white",
            activebackground="#c53030",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.delete_task
        )
        delete_btn.pack(side="right", fill="x", expand=True, padx=(6, 0))

        # ── Etiqueta de ayuda ──
        hint_label = tk.Label(
            self.root,
            text="💡 Doble clic en una tarea para marcarla como completada",
            font=("Helvetica", 9),
            bg="#f0f4f8",
            fg="#718096"
        )
        hint_label.pack(pady=(0, 10))

    # ──────────────────────────────────────────────
    # Lógica de la aplicación
    # ──────────────────────────────────────────────

    def add_task(self):
        """
        Añade una nueva tarea a la lista.
        Lee el texto del campo de entrada y lo agrega si no está vacío.
        """
        task_text = self.task_entry.get().strip()

        if not task_text:
            messagebox.showwarning("Campo vacío", "Por favor, escribe una tarea antes de añadir.")
            return

        # Guardar la tarea en la lista interna
        self.tasks.append({"text": task_text, "completed": False})

        # Mostrar la tarea en el Listbox
        self.task_listbox.insert(tk.END, f"  ○  {task_text}")

        # Limpiar el campo de entrada
        self.task_entry.delete(0, tk.END)
        self.task_entry.focus()

    def toggle_complete(self):
        """
        Alterna el estado completado/pendiente de la tarea seleccionada.
        Cambia el color y el símbolo visualmente para reflejar el nuevo estado.
        """
        selection = self.task_listbox.curselection()

        if not selection:
            messagebox.showinfo("Sin selección", "Por favor, selecciona una tarea de la lista.")
            return

        index = selection[0]
        task = self.tasks[index]

        if task["completed"]:
            # Volver a pendiente
            task["completed"] = False
            self.task_listbox.delete(index)
            self.task_listbox.insert(index, f"  ○  {task['text']}")
            self.task_listbox.itemconfig(index, fg="#2d3748")
        else:
            # Marcar como completada
            task["completed"] = True
            self.task_listbox.delete(index)
            self.task_listbox.insert(index, f"  ✔  {task['text']}")
            self.task_listbox.itemconfig(index, fg="#a0aec0")  # Gris para indicar completada

        # Mantener la selección en el mismo elemento
        self.task_listbox.selection_set(index)

    def delete_task(self):
        """
        Elimina la tarea seleccionada de la lista.
        Solicita confirmación antes de eliminar.
        """
        selection = self.task_listbox.curselection()

        if not selection:
            messagebox.showinfo("Sin selección", "Por favor, selecciona una tarea para eliminar.")
            return

        index = selection[0]
        task_text = self.tasks[index]["text"]

        # Confirmación antes de eliminar
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar la tarea?\n\n\"{task_text}\""
        )

        if confirm:
            self.tasks.pop(index)
            self.task_listbox.delete(index)


# ──────────────────────────────────────────────
# Punto de entrada de la aplicación
# ──────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()