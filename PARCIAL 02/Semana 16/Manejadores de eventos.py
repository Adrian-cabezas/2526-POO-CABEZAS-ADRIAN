"""
Aplicación GUI para Gestión de Tareas con Atajos de Teclado
Desarrollado con Python y Tkinter
"""

import tkinter as tk
from tkinter import messagebox, font


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Tareas")
        self.root.geometry("680x560")
        self.root.resizable(True, True)
        self.root.configure(bg="#1a1a2e")

        # Paleta de colores
        self.colors = {
            "bg_main":       "#1a1a2e",
            "bg_panel":      "#16213e",
            "bg_entry":      "#0f3460",
            "accent":        "#e94560",
            "accent_hover":  "#ff6b81",
            "btn_complete":  "#00b4d8",
            "btn_complete_h":"#48cae4",
            "btn_delete":    "#e94560",
            "btn_delete_h":  "#ff6b81",
            "text_primary":  "#eaeaea",
            "text_secondary":"#a0a0b8",
            "task_pending":  "#eaeaea",
            "task_done_bg":  "#0d3b2e",
            "task_done_fg":  "#52b788",
            "scrollbar":     "#0f3460",
            "border":        "#0f3460",
            "highlight":     "#e94560",
        }

        # Fuentes
        self.font_title   = font.Font(family="Courier New", size=20, weight="bold")
        self.font_subtitle= font.Font(family="Courier New", size=10)
        self.font_label   = font.Font(family="Courier New", size=10, weight="bold")
        self.font_entry   = font.Font(family="Courier New", size=12)
        self.font_task    = font.Font(family="Courier New", size=11)
        self.font_btn     = font.Font(family="Courier New", size=10, weight="bold")
        self.font_hint    = font.Font(family="Courier New", size=8)

        self._build_ui()
        self._bind_shortcuts()

    # ──────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ──────────────────────────────────────────

    def _build_ui(self):
        # ── Encabezado ──
        header = tk.Frame(self.root, bg=self.colors["bg_panel"], pady=18)
        header.pack(fill="x")

        tk.Label(
            header, text="◈ GESTOR DE TAREAS",
            font=self.font_title,
            bg=self.colors["bg_panel"],
            fg=self.colors["accent"]
        ).pack()

        tk.Label(
            header, text="gestión de tareas con atajos de teclado",
            font=self.font_subtitle,
            bg=self.colors["bg_panel"],
            fg=self.colors["text_secondary"]
        ).pack()

        # Línea decorativa
        tk.Frame(self.root, bg=self.colors["accent"], height=2).pack(fill="x")

        # ── Panel de entrada ──
        input_frame = tk.Frame(self.root, bg=self.colors["bg_main"], pady=16, padx=20)
        input_frame.pack(fill="x")

        tk.Label(
            input_frame, text="NUEVA TAREA",
            font=self.font_label,
            bg=self.colors["bg_main"],
            fg=self.colors["text_secondary"]
        ).pack(anchor="w", pady=(0, 6))

        entry_row = tk.Frame(input_frame, bg=self.colors["bg_main"])
        entry_row.pack(fill="x")

        # Campo de entrada con borde simulado
        entry_border = tk.Frame(entry_row, bg=self.colors["accent"], padx=2, pady=2)
        entry_border.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            entry_border,
            textvariable=self.entry_var,
            font=self.font_entry,
            bg=self.colors["bg_entry"],
            fg=self.colors["text_primary"],
            insertbackground=self.colors["accent"],
            relief="flat",
            bd=8
        )
        self.entry.pack(fill="x")

        self._make_button(
            entry_row, "＋  AÑADIR",
            self.colors["accent"], self.colors["accent_hover"],
            self.add_task
        ).pack(side="left")

        # ── Separador ──
        tk.Frame(self.root, bg=self.colors["border"], height=1).pack(fill="x", padx=20)

        # ── Contadores ──
        self.stats_frame = tk.Frame(self.root, bg=self.colors["bg_main"], pady=8, padx=20)
        self.stats_frame.pack(fill="x")

        self.lbl_pending  = tk.Label(self.stats_frame, font=self.font_hint,
                                     bg=self.colors["bg_main"], fg=self.colors["text_secondary"])
        self.lbl_pending.pack(side="left")
        self.lbl_done = tk.Label(self.stats_frame, font=self.font_hint,
                                  bg=self.colors["bg_main"], fg=self.colors["task_done_fg"])
        self.lbl_done.pack(side="left", padx=(16, 0))

        # ── Lista de tareas ──
        list_frame = tk.Frame(self.root, bg=self.colors["bg_main"], padx=20, pady=4)
        list_frame.pack(fill="both", expand=True)

        tk.Label(
            list_frame, text="TAREAS",
            font=self.font_label,
            bg=self.colors["bg_main"],
            fg=self.colors["text_secondary"]
        ).pack(anchor="w", pady=(0, 6))

        # Listbox + scrollbar
        lb_frame = tk.Frame(list_frame, bg=self.colors["border"], padx=2, pady=2)
        lb_frame.pack(fill="both", expand=True)

        inner = tk.Frame(lb_frame, bg=self.colors["bg_panel"])
        inner.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(inner, bg=self.colors["scrollbar"],
                                  troughcolor=self.colors["bg_main"],
                                  activebackground=self.colors["accent"])
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            inner,
            font=self.font_task,
            bg=self.colors["bg_panel"],
            fg=self.colors["task_pending"],
            selectbackground=self.colors["accent"],
            selectforeground="#ffffff",
            activestyle="none",
            relief="flat",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            cursor="hand2"
        )
        self.listbox.pack(fill="both", expand=True, padx=4, pady=4)
        scrollbar.config(command=self.listbox.yview)

        # ── Botones de acción ──
        btn_frame = tk.Frame(self.root, bg=self.colors["bg_main"], pady=14, padx=20)
        btn_frame.pack(fill="x")

        self._make_button(
            btn_frame, "✔  COMPLETAR  [C]",
            self.colors["btn_complete"], self.colors["btn_complete_h"],
            self.complete_task, width=22
        ).pack(side="left", padx=(0, 10))

        self._make_button(
            btn_frame, "✖  ELIMINAR  [Del/D]",
            self.colors["btn_delete"], self.colors["btn_delete_h"],
            self.delete_task, width=22
        ).pack(side="left")

        # ── Barra de atajos ──
        hints_bar = tk.Frame(self.root, bg=self.colors["bg_panel"], pady=6)
        hints_bar.pack(fill="x", side="bottom")

        hints = "Enter: añadir   |   C: completar   |   Del / D: eliminar   |   Esc: cerrar"
        tk.Label(
            hints_bar, text=hints,
            font=self.font_hint,
            bg=self.colors["bg_panel"],
            fg=self.colors["text_secondary"]
        ).pack()

        # ── Estado interno ──
        self.tasks = []          # lista de dicts {text, done}
        self._update_stats()

    # ──────────────────────────────────────────
    #  WIDGET HELPER
    # ──────────────────────────────────────────

    def _make_button(self, parent, text, color, hover_color, command, width=14):
        btn = tk.Button(
            parent, text=text,
            font=self.font_btn,
            bg=color, fg="#ffffff",
            activebackground=hover_color,
            activeforeground="#ffffff",
            relief="flat", bd=0,
            padx=14, pady=8,
            width=width,
            cursor="hand2",
            command=command
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    # ──────────────────────────────────────────
    #  ATAJOS DE TECLADO
    # ──────────────────────────────────────────

    def _bind_shortcuts(self):
        self.root.bind("<Return>",  lambda e: self.add_task())
        self.root.bind("<c>",       lambda e: self.complete_task())
        self.root.bind("<C>",       lambda e: self.complete_task())
        self.root.bind("<Delete>",  lambda e: self.delete_task())
        self.root.bind("<d>",       lambda e: self.delete_task())
        self.root.bind("<D>",       lambda e: self.delete_task())
        self.root.bind("<Escape>",  lambda e: self._quit())

    # ──────────────────────────────────────────
    #  LÓGICA DE TAREAS
    # ──────────────────────────────────────────

    def add_task(self):
        text = self.entry_var.get().strip()
        if not text:
            self._flash_entry()
            return
        self.tasks.append({"text": text, "done": False})
        self._refresh_listbox()
        self.entry_var.set("")
        self.entry.focus()
        self._update_stats()

    def complete_task(self):
        idx = self._selected_index()
        if idx is None:
            return
        self.tasks[idx]["done"] = not self.tasks[idx]["done"]   # toggle
        self._refresh_listbox()
        self.listbox.selection_set(idx)
        self._update_stats()

    def delete_task(self):
        idx = self._selected_index()
        if idx is None:
            return
        del self.tasks[idx]
        self._refresh_listbox()
        # Seleccionar el elemento anterior (si existe)
        new_idx = min(idx, len(self.tasks) - 1)
        if new_idx >= 0:
            self.listbox.selection_set(new_idx)
        self._update_stats()

    # ──────────────────────────────────────────
    #  ACTUALIZACIÓN DE LA VISTA
    # ──────────────────────────────────────────

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            prefix = "✔  " if task["done"] else "○  "
            self.listbox.insert(tk.END, f"  {prefix}{task['text']}")

        # Colorear cada fila individualmente
        for i, task in enumerate(self.tasks):
            if task["done"]:
                self.listbox.itemconfig(
                    i,
                    fg=self.colors["task_done_fg"],
                    bg=self.colors["task_done_bg"]
                )
            else:
                self.listbox.itemconfig(
                    i,
                    fg=self.colors["task_pending"],
                    bg=self.colors["bg_panel"]
                )

    def _update_stats(self):
        total   = len(self.tasks)
        done    = sum(1 for t in self.tasks if t["done"])
        pending = total - done
        self.lbl_pending.config(text=f"◆ Pendientes: {pending}")
        self.lbl_done.config(text=f"◆ Completadas: {done}")

    def _selected_index(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo(
                "Sin selección",
                "Por favor, selecciona una tarea de la lista.",
                parent=self.root
            )
            return None
        return sel[0]

    def _flash_entry(self):
        """Parpadeo rojo en el campo de entrada si está vacío."""
        original = self.colors["accent"]
        warn     = "#ff0000"
        self.entry.master.config(bg=warn)
        self.root.after(200, lambda: self.entry.master.config(bg=original))

    def _quit(self):
        if messagebox.askyesno(
            "Cerrar aplicación",
            "¿Deseas cerrar el gestor de tareas?",
            parent=self.root
        ):
            self.root.destroy()


# ──────────────────────────────────────────
#  PUNTO DE ENTRADA
# ──────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()