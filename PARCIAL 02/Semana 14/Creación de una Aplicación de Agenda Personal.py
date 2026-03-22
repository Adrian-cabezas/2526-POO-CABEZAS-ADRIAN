"""
Aplicación de Agenda Personal
Desarrollada con Tkinter en Python

Funcionalidades:
- Agregar eventos con fecha, hora y descripción
- Ver eventos en una lista (TreeView)
- Eliminar eventos seleccionados
- DatePicker para selección de fechas
- Confirmación antes de eliminar
- Organización con Frames (contenedores)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, date


# ──────────────────────────────────────────────
#  Widget DatePicker personalizado
# ──────────────────────────────────────────────
class DatePicker(tk.Toplevel):
    """Ventana emergente que permite seleccionar una fecha en un calendario visual."""

    def __init__(self, parent, callback):
        """
        Inicializa el DatePicker.

        Args:
            parent: Widget padre de Tkinter.
            callback: Función a llamar con la fecha seleccionada (string "DD/MM/YYYY").
        """
        super().__init__(parent)
        self.callback = callback
        self.title("Seleccionar Fecha")
        self.resizable(False, False)
        self.grab_set()  # Bloquea la ventana principal mientras el calendario está abierto

        # Fecha inicial: hoy
        today = date.today()
        self.current_year = today.year
        self.current_month = today.month

        self._build_ui()
        self._draw_calendar()

    def _build_ui(self):
        """Construye los controles de navegación y la cuadrícula del calendario."""
        # ── Frame de navegación (mes / año) ──
        nav_frame = tk.Frame(self, bg="#2b3a4a", pady=6)
        nav_frame.pack(fill="x")

        btn_style = {"bg": "#3d5166", "fg": "white", "relief": "flat",
                     "font": ("Courier New", 11, "bold"), "cursor": "hand2",
                     "padx": 8, "pady": 2}

        tk.Button(nav_frame, text="◀", command=self._prev_month, **btn_style).pack(side="left", padx=8)

        self.month_year_label = tk.Label(
            nav_frame, text="", bg="#2b3a4a", fg="white",
            font=("Courier New", 11, "bold"), width=18
        )
        self.month_year_label.pack(side="left", expand=True)

        tk.Button(nav_frame, text="▶", command=self._next_month, **btn_style).pack(side="right", padx=8)

        # ── Frame de días de la semana ──
        days_frame = tk.Frame(self, bg="#1e2d3d")
        days_frame.pack(fill="x")

        for col, day in enumerate(["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]):
            color = "#e74c3c" if day in ("Sa", "Do") else "#7fb3d3"
            tk.Label(
                days_frame, text=day, bg="#1e2d3d", fg=color,
                font=("Courier New", 9, "bold"), width=4
            ).grid(row=0, column=col, padx=2, pady=4)

        # ── Frame de celdas del calendario ──
        self.cal_frame = tk.Frame(self, bg="#1e2d3d")
        self.cal_frame.pack(padx=8, pady=4)

    def _draw_calendar(self):
        """Dibuja las celdas de días del mes actual."""
        # Limpiar celdas anteriores
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        # Actualizar etiqueta de mes/año
        month_names = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        self.month_year_label.config(
            text=f"{month_names[self.current_month - 1]} {self.current_year}"
        )

        today = date.today()
        month_cal = calendar.monthcalendar(self.current_year, self.current_month)

        for row_idx, week in enumerate(month_cal):
            for col_idx, day_num in enumerate(week):
                if day_num == 0:
                    # Celda vacía (días fuera del mes)
                    tk.Label(self.cal_frame, text="", bg="#1e2d3d", width=4, height=2).grid(
                        row=row_idx, column=col_idx, padx=1, pady=1
                    )
                    continue

                # Determinar colores según contexto
                is_today = (
                    day_num == today.day and
                    self.current_month == today.month and
                    self.current_year == today.year
                )
                is_weekend = col_idx >= 5

                if is_today:
                    bg, fg = "#e67e22", "white"
                elif is_weekend:
                    bg, fg = "#2c3e50", "#e74c3c"
                else:
                    bg, fg = "#2c3e50", "#ecf0f1"

                btn = tk.Button(
                    self.cal_frame,
                    text=str(day_num),
                    width=4, height=2,
                    bg=bg, fg=fg,
                    relief="flat",
                    font=("Courier New", 9),
                    cursor="hand2",
                    activebackground="#3498db",
                    activeforeground="white",
                    command=lambda d=day_num: self._select_date(d)
                )
                btn.grid(row=row_idx, column=col_idx, padx=1, pady=1)

    def _prev_month(self):
        """Navega al mes anterior."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._draw_calendar()

    def _next_month(self):
        """Navega al mes siguiente."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._draw_calendar()

    def _select_date(self, day):
        """
        Llama al callback con la fecha seleccionada y cierra el DatePicker.

        Args:
            day (int): Día seleccionado.
        """
        selected = f"{day:02d}/{self.current_month:02d}/{self.current_year}"
        self.callback(selected)
        self.destroy()


# ──────────────────────────────────────────────
#  Aplicación Principal
# ──────────────────────────────────────────────
class AgendaPersonal:
    """Aplicación de Agenda Personal construida con Tkinter."""

    def __init__(self, root):
        """
        Inicializa la aplicación.

        Args:
            root: Ventana raíz de Tkinter.
        """
        self.root = root
        self.root.title("📅 Agenda Personal")
        self.root.geometry("850x620")
        self.root.resizable(True, True)
        self.root.configure(bg="#1a2533")
        self.root.minsize(700, 500)

        # Lista interna de eventos
        self.events = []

        self._build_ui()

    # ──────────────────────────────────────────
    #  Construcción de la Interfaz
    # ──────────────────────────────────────────
    def _build_ui(self):
        """Construye todos los contenedores y widgets de la interfaz."""
        self._build_header()
        self._build_main_area()

    def _build_header(self):
        """Construye el encabezado de la aplicación."""
        header = tk.Frame(self.root, bg="#0f1923", height=60, pady=10)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📅  AGENDA PERSONAL",
            bg="#0f1923", fg="#3498db",
            font=("Courier New", 18, "bold")
        ).pack(side="left", padx=24)

        # Etiqueta de fecha/hora actual (se actualiza cada segundo)
        self.clock_label = tk.Label(
            header, text="", bg="#0f1923", fg="#7fb3d3",
            font=("Courier New", 11)
        )
        self.clock_label.pack(side="right", padx=24)
        self._update_clock()

    def _build_main_area(self):
        """Construye el área principal con los tres frames funcionales."""
        main = tk.Frame(self.root, bg="#1a2533")
        main.pack(fill="both", expand=True, padx=16, pady=10)

        # ── Frame izquierdo: TreeView de eventos ──
        self._build_list_frame(main)

        # ── Frame derecho: entrada de datos + acciones ──
        right_panel = tk.Frame(main, bg="#1a2533")
        right_panel.pack(side="right", fill="both", padx=(12, 0))

        self._build_input_frame(right_panel)
        self._build_action_frame(right_panel)

    def _build_list_frame(self, parent):
        """
        Construye el Frame de visualización de eventos (TreeView).

        Args:
            parent: Widget padre donde se empaqueta el frame.
        """
        list_frame = tk.LabelFrame(
            parent,
            text="  📋 Eventos Programados  ",
            bg="#1e2d3d", fg="#3498db",
            font=("Courier New", 11, "bold"),
            relief="flat",
            bd=2,
            labelanchor="n"
        )
        list_frame.pack(side="left", fill="both", expand=True)

        # ── TreeView ──
        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=18)

        # Encabezados
        self.tree.heading("fecha",       text="📅 Fecha")
        self.tree.heading("hora",        text="🕐 Hora")
        self.tree.heading("descripcion", text="📝 Descripción")

        # Anchos de columna
        self.tree.column("fecha",       width=100, anchor="center", minwidth=80)
        self.tree.column("hora",        width=80,  anchor="center", minwidth=60)
        self.tree.column("descripcion", width=260, anchor="w",      minwidth=150)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scrollbar.pack(side="right", fill="y", pady=8, padx=(0, 4))

        # Estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         background="#1e2d3d",
                         foreground="#ecf0f1",
                         rowheight=28,
                         fieldbackground="#1e2d3d",
                         font=("Courier New", 10))
        style.configure("Treeview.Heading",
                         background="#0f1923",
                         foreground="#3498db",
                         font=("Courier New", 10, "bold"),
                         relief="flat")
        style.map("Treeview",
                  background=[("selected", "#2980b9")],
                  foreground=[("selected", "white")])

        # Alternar colores de filas
        self.tree.tag_configure("even", background="#253545")
        self.tree.tag_configure("odd",  background="#1e2d3d")

    def _build_input_frame(self, parent):
        """
        Construye el Frame de entrada de datos (fecha, hora, descripción).

        Args:
            parent: Widget padre donde se empaqueta el frame.
        """
        input_frame = tk.LabelFrame(
            parent,
            text="  ➕ Nuevo Evento  ",
            bg="#1e2d3d", fg="#2ecc71",
            font=("Courier New", 11, "bold"),
            relief="flat",
            bd=2,
            labelanchor="n"
        )
        input_frame.pack(fill="x", pady=(0, 10))

        pad = {"padx": 12, "pady": 5}

        # ── Campo: Fecha ──
        tk.Label(input_frame, text="📅 Fecha:", bg="#1e2d3d", fg="#bdc3c7",
                 font=("Courier New", 10)).grid(row=0, column=0, sticky="w", **pad)

        date_row = tk.Frame(input_frame, bg="#1e2d3d")
        date_row.grid(row=0, column=1, sticky="ew", **pad)
        input_frame.columnconfigure(1, weight=1)

        self.date_var = tk.StringVar()
        self.date_entry = tk.Entry(
            date_row, textvariable=self.date_var,
            bg="#2c3e50", fg="#ecf0f1", insertbackground="white",
            font=("Courier New", 10), relief="flat",
            width=13
        )
        self.date_entry.pack(side="left")
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        tk.Button(
            date_row, text="🗓",
            command=self._open_datepicker,
            bg="#3d5166", fg="white", relief="flat",
            font=("Courier New", 10), cursor="hand2",
            padx=6
        ).pack(side="left", padx=(4, 0))

        # ── Campo: Hora ──
        tk.Label(input_frame, text="🕐 Hora:", bg="#1e2d3d", fg="#bdc3c7",
                 font=("Courier New", 10)).grid(row=1, column=0, sticky="w", **pad)

        self.time_var = tk.StringVar()
        self.time_entry = tk.Entry(
            input_frame, textvariable=self.time_var,
            bg="#2c3e50", fg="#ecf0f1", insertbackground="white",
            font=("Courier New", 10), relief="flat", width=13
        )
        self.time_entry.grid(row=1, column=1, sticky="w", **pad)
        self.time_entry.insert(0, "HH:MM")

        # Placeholder behavior para hora
        self.time_entry.bind("<FocusIn>",  self._on_time_focus_in)
        self.time_entry.bind("<FocusOut>", self._on_time_focus_out)

        # ── Campo: Descripción ──
        tk.Label(input_frame, text="📝 Descripción:", bg="#1e2d3d", fg="#bdc3c7",
                 font=("Courier New", 10)).grid(row=2, column=0, sticky="nw", **pad)

        self.desc_text = tk.Text(
            input_frame,
            bg="#2c3e50", fg="#ecf0f1", insertbackground="white",
            font=("Courier New", 10), relief="flat",
            width=22, height=4, wrap="word"
        )
        self.desc_text.grid(row=2, column=1, sticky="ew", **pad)

    def _build_action_frame(self, parent):
        """
        Construye el Frame de botones de acción.

        Args:
            parent: Widget padre donde se empaqueta el frame.
        """
        action_frame = tk.LabelFrame(
            parent,
            text="  ⚡ Acciones  ",
            bg="#1e2d3d", fg="#e67e22",
            font=("Courier New", 11, "bold"),
            relief="flat",
            bd=2,
            labelanchor="n"
        )
        action_frame.pack(fill="x")

        btn_cfg = {"font": ("Courier New", 10, "bold"), "relief": "flat",
                   "cursor": "hand2", "pady": 8, "padx": 6}

        # ── Botón: Agregar Evento ──
        tk.Button(
            action_frame,
            text="➕  Agregar Evento",
            bg="#27ae60", fg="white",
            activebackground="#2ecc71",
            command=self._add_event,
            **btn_cfg
        ).pack(fill="x", padx=12, pady=(12, 5))

        # ── Botón: Eliminar Evento Seleccionado ──
        tk.Button(
            action_frame,
            text="🗑  Eliminar Evento Seleccionado",
            bg="#c0392b", fg="white",
            activebackground="#e74c3c",
            command=self._delete_event,
            **btn_cfg
        ).pack(fill="x", padx=12, pady=5)

        # ── Botón: Salir ──
        tk.Button(
            action_frame,
            text="✖  Salir",
            bg="#7f8c8d", fg="white",
            activebackground="#95a5a6",
            command=self._exit_app,
            **btn_cfg
        ).pack(fill="x", padx=12, pady=(5, 12))

    # ──────────────────────────────────────────
    #  Lógica de Eventos
    # ──────────────────────────────────────────
    def _add_event(self):
        """
        Valida los campos y agrega un nuevo evento a la lista.
        Actualiza el TreeView con el evento recién añadido.
        """
        fecha = self.date_var.get().strip()
        hora  = self.time_var.get().strip()
        desc  = self.desc_text.get("1.0", "end").strip()

        # ── Validaciones ──
        if not fecha:
            messagebox.showwarning("Campo vacío", "Por favor ingresa una fecha.")
            return

        if not self._validate_date(fecha):
            messagebox.showerror(
                "Fecha inválida",
                "El formato de fecha debe ser DD/MM/YYYY.\nEjemplo: 25/12/2025"
            )
            return

        if not hora or hora == "HH:MM":
            messagebox.showwarning("Campo vacío", "Por favor ingresa una hora.")
            return

        if not self._validate_time(hora):
            messagebox.showerror(
                "Hora inválida",
                "El formato de hora debe ser HH:MM (24 h).\nEjemplo: 14:30"
            )
            return

        if not desc:
            messagebox.showwarning("Campo vacío", "Por favor ingresa una descripción.")
            return

        # ── Agregar evento ──
        event = {"fecha": fecha, "hora": hora, "descripcion": desc}
        self.events.append(event)
        self._refresh_treeview()
        self._clear_inputs()

        messagebox.showinfo("Éxito", f"✅ Evento agregado correctamente:\n{fecha} a las {hora}")

    def _delete_event(self):
        """
        Elimina el evento seleccionado en el TreeView.
        Muestra un diálogo de confirmación antes de proceder.
        """
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Sin selección",
                "Por favor selecciona un evento de la lista para eliminar."
            )
            return

        # ── Diálogo de confirmación ──
        item = self.tree.item(selected[0])
        fecha, hora, desc = item["values"]
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar este evento?\n\n"
            f"📅 Fecha: {fecha}\n"
            f"🕐 Hora:  {hora}\n"
            f"📝 Desc:  {desc[:60]}{'...' if len(desc) > 60 else ''}"
        )

        if confirm:
            # Encontrar y eliminar de la lista interna
            idx = self.tree.index(selected[0])
            if 0 <= idx < len(self.events):
                self.events.pop(idx)
            self._refresh_treeview()
            messagebox.showinfo("Eliminado", "🗑 Evento eliminado correctamente.")

    def _exit_app(self):
        """Confirma y cierra la aplicación."""
        if messagebox.askyesno("Salir", "¿Deseas salir de la Agenda Personal?"):
            self.root.destroy()

    # ──────────────────────────────────────────
    #  Utilidades internas
    # ──────────────────────────────────────────
    def _refresh_treeview(self):
        """Limpia y vuelve a poblar el TreeView con la lista actual de eventos."""
        # Eliminar todas las filas
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ordenar eventos por fecha y hora
        def sort_key(e):
            try:
                dt = datetime.strptime(f"{e['fecha']} {e['hora']}", "%d/%m/%Y %H:%M")
                return dt
            except ValueError:
                return datetime.max

        self.events.sort(key=sort_key)

        # Insertar filas con colores alternados
        for i, event in enumerate(self.events):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert(
                "", "end",
                values=(event["fecha"], event["hora"], event["descripcion"]),
                tags=(tag,)
            )

    def _clear_inputs(self):
        """Limpia los campos de entrada después de agregar un evento."""
        self.date_var.set(datetime.now().strftime("%d/%m/%Y"))
        self.time_var.set("HH:MM")
        self.time_entry.config(fg="#7f8c8d")
        self.desc_text.delete("1.0", "end")

    def _open_datepicker(self):
        """Abre el DatePicker y asigna la fecha seleccionada al campo correspondiente."""
        DatePicker(self.root, callback=lambda d: self.date_var.set(d))

    def _update_clock(self):
        """Actualiza la etiqueta del reloj cada segundo."""
        now = datetime.now().strftime("%A, %d/%m/%Y  %H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self._update_clock)

    def _on_time_focus_in(self, event):
        """Borra el placeholder de hora cuando el campo recibe el foco."""
        if self.time_var.get() == "HH:MM":
            self.time_entry.delete(0, "end")
            self.time_entry.config(fg="#ecf0f1")

    def _on_time_focus_out(self, event):
        """Restaura el placeholder de hora si el campo queda vacío."""
        if not self.time_var.get().strip():
            self.time_entry.insert(0, "HH:MM")
            self.time_entry.config(fg="#7f8c8d")

    # ──────────────────────────────────────────
    #  Validadores
    # ──────────────────────────────────────────
    @staticmethod
    def _validate_date(date_str: str) -> bool:
        """
        Verifica que la cadena tenga formato DD/MM/YYYY y sea una fecha válida.

        Args:
            date_str (str): Cadena de fecha a validar.

        Returns:
            bool: True si la fecha es válida, False en caso contrario.
        """
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def _validate_time(time_str: str) -> bool:
        """
        Verifica que la cadena tenga formato HH:MM válido (24 horas).

        Args:
            time_str (str): Cadena de hora a validar.

        Returns:
            bool: True si la hora es válida, False en caso contrario.
        """
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False


# ──────────────────────────────────────────────
#  Punto de entrada
# ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaPersonal(root)
    root.mainloop()