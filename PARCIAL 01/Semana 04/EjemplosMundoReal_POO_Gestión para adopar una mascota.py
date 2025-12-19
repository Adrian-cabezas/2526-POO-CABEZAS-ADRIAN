"""
Sistema de adopción de mascotas (POO) — Interfaz estética sin dependencias externas

Este archivo implementa un pequeño sistema orientado a objetos para gestionar adopciones
de mascotas.

Clases principales:
- Pet: representa una mascota (atributos + métodos para cambiar estado).
- Adopter: representa a una persona que adopta (valida si puede aplicar).
- AdoptionApplication: representa una solicitud de adopción (gestiona estados).
- Shelter: orquesta mascotas, adoptantes y solicitudes (crea/revisa/finaliza solicitudes).
- PrettyUI: capa de presentación que imprime tablas, paneles y fichas con estilo
            usando solo Unicode y ANSI (sin dependencias externas).

Para ejecutar:
    python pet_adoption_no_rich.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Sequence, Any
import uuid
import shutil
import sys

# -------------------------
# Utilidades internas
# -------------------------
def _new_id(short: bool = True) -> str:
    """Genera un id legible (acortado)."""
    return str(uuid.uuid4())[:8] if short else str(uuid.uuid4())

def _term_width(default: int = 80) -> int:
    """Devuelve el ancho del terminal o un valor por defecto."""
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return default

# ANSI colors simples (si la terminal los soporta)
ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}

def color(text: str, col: Optional[str]) -> str:
    """Aplica color ANSI al texto si se indica un nombre válido; si col es None, devuelve texto sin cambios."""
    if not col or col not in ANSI:
        return text
    return f"{ANSI[col]}{text}{ANSI['reset']}"

# -------------------------
# MODELO (POO)
# -------------------------
@dataclass
class Pet:
    """
    Representa una mascota en el refugio.
    - name, species, breed, age_years, vaccinated, neutered, notes, pet_id, status
    - Métodos para cambiar estado y comprobar si adoptable.
    """
    name: str
    species: str
    breed: str
    age_years: float
    vaccinated: bool = False
    neutered: bool = False
    notes: str = ""
    pet_id: str = field(default_factory=_new_id)
    status: str = field(default="available")  # available | pending | adopted | unavailable

    def is_adoptable(self) -> bool:
        return self.status == "available"

    def mark_pending(self) -> None:
        if not self.is_adoptable():
            raise ValueError("La mascota no está disponible para marcar como pendiente.")
        self.status = "pending"

    def mark_adopted(self) -> None:
        self.status = "adopted"

    def mark_available(self) -> None:
        self.status = "available"

    def short_summary(self) -> str:
        vac = "Sí" if self.vaccinated else "No"
        neu = "Sí" if self.neutered else "No"
        return f"{self.pet_id} | {self.name} — {self.species}/{self.breed} — {self.age_years:.1f} años — Vac:{vac} — Est:{neu} — Estado:{self.status}"

@dataclass
class Adopter:
    """
    Representa a un adoptante.
    - name, contact, adopter_id, adopted_pets, max_active_applications
    - can_apply(shelter): valida si puede crear otra solicitud activa
    """
    name: str
    contact: str
    adopter_id: str = field(default_factory=_new_id)
    adopted_pets: List[str] = field(default_factory=list)
    max_active_applications: int = 3

    def can_apply(self, shelter: "Shelter") -> bool:
        active = [a for a in shelter.applications.values()
                  if a.adopter_id == self.adopter_id and a.status in ("submitted", "under_review")]
        return len(active) < self.max_active_applications

    def __str__(self) -> str:
        return f"{self.name} [{self.adopter_id}] — {self.contact} — Previas: {len(self.adopted_pets)}"

@dataclass
class AdoptionApplication:
    """
    Representa una solicitud de adopción.
    - pet_id, adopter_id, message, application_id, submitted_at, status, reviewed_by, reviewed_at
    - Métodos para transitar estados: mark_under_review, approve, reject, complete, cancel
    """
    pet_id: str
    adopter_id: str
    message: str = ""
    application_id: str = field(default_factory=_new_id)
    submitted_at: datetime = field(default_factory=datetime.now)
    status: str = field(default="submitted")  # submitted | under_review | approved | rejected | completed | cancelled
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None

    def mark_under_review(self, reviewer: Optional[str] = None) -> None:
        if self.status != "submitted":
            raise ValueError("Solo solicitudes 'submitted' pueden ponerse en revisión.")
        self.status = "under_review"
        self.reviewed_by = reviewer
        self.reviewed_at = datetime.now()

    def approve(self, reviewer: Optional[str] = None) -> None:
        if self.status not in ("submitted", "under_review"):
            raise ValueError("Solo solicitudes 'submitted' o 'under_review' pueden aprobarse.")
        self.status = "approved"
        self.reviewed_by = reviewer or self.reviewed_by
        self.reviewed_at = datetime.now()

    def reject(self, reviewer: Optional[str] = None, reason: str = "") -> None:
        if self.status not in ("submitted", "under_review"):
            raise ValueError("Solo solicitudes 'submitted' o 'under_review' pueden rechazarse.")
        self.status = "rejected"
        self.reviewed_by = reviewer or self.reviewed_by
        self.reviewed_at = datetime.now()
        if reason:
            self.message += f"\n[Motivo rechazo: {reason}]"

    def complete(self) -> None:
        if self.status != "approved":
            raise ValueError("Solo solicitudes aprobadas pueden completarse.")
        self.status = "completed"

    def cancel(self) -> None:
        if self.status in ("completed", "cancelled"):
            raise ValueError("Solicitud ya terminada.")
        self.status = "cancelled"

    def short_summary(self) -> str:
        return f"{self.application_id} | Pet:{self.pet_id} | Adopter:{self.adopter_id} | Estado:{self.status} | Envío:{self.submitted_at.date()}"

# -------------------------
# SHELTER: reglas de negocio
# -------------------------
class Shelter:
    """
    Orquesta mascotas, adoptantes y solicitudes.
    Métodos:
    - add_pet, find_pet, list_available_pets
    - register_adopter, find_adopter
    - create_application, review_application, finalize_adoption, cancel_application
    - list_applications
    """
    def __init__(self, name: str):
        self.name = name
        self.pets: Dict[str, Pet] = {}
        self.adopters: Dict[str, Adopter] = {}
        self.applications: Dict[str, AdoptionApplication] = {}

    # Mascotas
    def add_pet(self, pet: Pet) -> None:
        if pet.pet_id in self.pets:
            raise KeyError("Pet ID ya existe.")
        self.pets[pet.pet_id] = pet

    def find_pet(self, pet_id: str) -> Pet:
        if pet_id not in self.pets:
            raise KeyError("Mascota no encontrada.")
        return self.pets[pet_id]

    def list_available_pets(self) -> List[Pet]:
        return [p for p in self.pets.values() if p.is_adoptable()]

    # Adoptantes
    def register_adopter(self, adopter: Adopter) -> None:
        if adopter.adopter_id in self.adopters:
            raise KeyError("Adoptante ya registrado.")
        self.adopters[adopter.adopter_id] = adopter

    def find_adopter(self, adopter_id: str) -> Adopter:
        if adopter_id not in self.adopters:
            raise KeyError("Adoptante no encontrado.")
        return self.adopters[adopter_id]

    # Solicitudes
    def create_application(self, adopter_id: str, pet_id: str, message: str = "") -> AdoptionApplication:
        adopter = self.find_adopter(adopter_id)
        pet = self.find_pet(pet_id)

        if not pet.is_adoptable():
            raise ValueError("La mascota no está disponible para adopción.")
        if not adopter.can_apply(self):
            raise ValueError("El adoptante tiene demasiadas solicitudes activas.")

        app = AdoptionApplication(pet_id=pet_id, adopter_id=adopter_id, message=message)
        self.applications[app.application_id] = app

        # Reservamos la mascota mientras se revisa
        pet.mark_pending()
        return app

    def review_application(self, application_id: str, action: str, reviewer: Optional[str] = None, reason: str = "") -> AdoptionApplication:
        if application_id not in self.applications:
            raise KeyError("Solicitud no encontrada.")
        app = self.applications[application_id]
        pet = self.find_pet(app.pet_id)

        if action == "under_review":
            app.mark_under_review(reviewer)
        elif action == "approve":
            app.approve(reviewer)
        elif action == "reject":
            app.reject(reviewer, reason)
            pet.mark_available()
        else:
            raise ValueError("Acción desconocida en revisión.")

        return app

    def finalize_adoption(self, application_id: str) -> None:
        if application_id not in self.applications:
            raise KeyError("Solicitud no encontrada.")
        app = self.applications[application_id]
        if app.status != "approved":
            raise ValueError("Solo solicitudes aprobadas pueden finalizarse.")
        pet = self.find_pet(app.pet_id)
        adopter = self.find_adopter(app.adopter_id)

        pet.mark_adopted()
        adopter.adopted_pets.append(pet.pet_id)
        app.complete()

    def cancel_application(self, application_id: str) -> None:
        if application_id not in self.applications:
            raise KeyError("Solicitud no encontrada.")
        app = self.applications[application_id]
        if app.status in ("completed", "cancelled"):
            raise ValueError("Solicitud ya terminada.")
        pet = self.find_pet(app.pet_id)
        app.cancel()
        if pet.status == "pending":
            pet.mark_available()

    def list_applications(self, status_filter: Optional[str] = None) -> List[AdoptionApplication]:
        apps = list(self.applications.values())
        if status_filter:
            apps = [a for a in apps if a.status == status_filter]
        return apps

    def __str__(self) -> str:
        return f"{self.name} — Mascotas: {len(self.pets)} (Disponibles: {len(self.list_available_pets())}), Adoptantes: {len(self.adopters)}, Solicitudes: {len(self.applications)}"

# -------------------------
# PRESENTACIÓN: PrettyUI sin rich
# -------------------------
class PrettyUI:
    """
    Capa de presentación que crea salidas estéticas sin librerías externas.
    - Usa bordes Unicode, tablas alineadas y colores ANSI sencillos.
    - Si la terminal no soporta colores, los códigos ANSI seguirán impresos (no afectan la lógica).
    """
    def __init__(self, shelter: Shelter):
        self.shelter = shelter
        self.width = max(60, _term_width())

    # Encabezado con borde y título centrado
    def header(self, title: str) -> None:
        pad = 4
        inner_width = min(self.width - 4, max(len(title) + pad, 40))
        line = "═" * inner_width
        print(color("╔" + line + "╗", "cyan"))
        print(color("║" + title.center(inner_width) + "║", "cyan"))
        print(color("╚" + line + "╝", "cyan"))

    # Panel de texto (como un recuadro)
    def panel(self, title: str, lines: Sequence[str], style: Optional[str] = "green") -> None:
        content_width = min(self.width - 6, max((len(l) for l in lines), default=0, key=lambda x: x) if lines else len(title))
        content_width = max(content_width, len(title) + 2)
        top = "┌" + "─" * (content_width + 2) + "┐"
        bot = "└" + "─" * (content_width + 2) + "┘"
        print(color(top, style))
        # título en la esquina superior izquierda
        title_line = f" {title} "
        print(color("│ " + title_line.ljust(content_width + 1) + "│", style))
        print(color("├" + "─" * (content_width + 2) + "┤", style))
        for l in lines:
            # cortar si es muy largo
            chunk = l if len(l) <= content_width else l[:content_width - 3] + "..."
            print(color("│ " + chunk.ljust(content_width + 1) + "│", style))
        print(color(bot, style))

    # Tabla genérica: headers + rows (ajusta anchos automáticamente)
    def table(self, headers: Sequence[str], rows: Sequence[Sequence[Any]], title: Optional[str] = None) -> None:
        # Convertir a string y calcular anchos
        str_rows = [[str(c) for c in row] for row in rows]
        cols = len(headers)
        col_widths = [len(h) for h in headers]
        for r in str_rows:
            for i in range(cols):
                val = r[i] if i < len(r) else ""
                col_widths[i] = max(col_widths[i], len(val))
        total_width = sum(col_widths) + 3 * cols + 1
        total_width = min(total_width, self.width - 4)
        # construir bordes
        top = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
        mid = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
        bot = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"
        if title:
            print(color(title.center(self.width), "magenta"))
        print(color(top, "blue"))
        # header
        header_cells = []
        for i, h in enumerate(headers):
            header_cells.append(" " + h.ljust(col_widths[i]) + " ")
        print(color("│" + "│".join(header_cells) + "│", "bold"))
        print(color(mid, "blue"))
        # rows
        for r in str_rows:
            cells = []
            for i in range(cols):
                val = r[i] if i < len(r) else ""
                cells.append(" " + val.ljust(col_widths[i]) + " ")
            print("│" + "│".join(cells) + "│")
        print(color(bot, "blue"))

    # Vistas concretas
    def show_summary(self) -> None:
        self.panel("Resumen del refugio", [str(self.shelter)], style="green")

    def show_pets(self, only_available: bool = False) -> None:
        pets = self.shelter.list_available_pets() if only_available else list(self.shelter.pets.values())
        title = "Mascotas disponibles" if only_available else "Todas las mascotas"
        headers = ["ID", "Nombre", "Especie", "Raza", "Edad", "Vac.", "Ester.", "Estado"]
        rows = []
        for p in pets:
            rows.append([p.pet_id, p.name, p.species, p.breed, f"{p.age_years:.1f}", "Sí" if p.vaccinated else "No", "Sí" if p.neutered else "No", p.status])
        self.table(headers, rows, title=title)
        print()  # separación

    def show_adopters(self) -> None:
        headers = ["ID", "Nombre", "Contacto", "Adopciones previas"]
        rows = []
        for a in self.shelter.adopters.values():
            rows.append([a.adopter_id, a.name, a.contact, str(len(a.adopted_pets))])
        self.table(headers, rows, title="Adoptantes")
        print()

    def show_applications(self, status_filter: Optional[str] = None) -> None:
        apps = self.shelter.list_applications(status_filter)
        title = "Solicitudes" + (f" — {status_filter}" if status_filter else "")
        headers = ["ID", "Mascota", "Adoptante", "Envío", "Estado", "Revisor"]
        rows = []
        for a in apps:
            pet_name = self.shelter.pets.get(a.pet_id).name if a.pet_id in self.shelter.pets else "Desconocida"
            rows.append([a.application_id, f"{pet_name} ({a.pet_id})", a.adopter_id, a.submitted_at.strftime("%Y-%m-%d"), a.status, a.reviewed_by or "-"])
        self.table(headers, rows, title=title)
        print()

    def pet_card(self, pet_id: str) -> None:
        try:
            pet = self.shelter.find_pet(pet_id)
        except KeyError:
            print(color("Mascota no encontrada.", "red"))
            return
        lines = [
            f"Nombre : {pet.name}",
            f"ID     : {pet.pet_id}",
            f"Especie: {pet.species}",
            f"Raza   : {pet.breed}",
            f"Edad   : {pet.age_years:.1f} años",
            f"Vacunado   : {'Sí' if pet.vaccinated else 'No'}",
            f"Esterilizado: {'Sí' if pet.neutered else 'No'}",
            "",
            f"Estado: {pet.status}",
            "",
            "Observaciones:",
            pet.notes or "—"
        ]
        self.panel(f"MASCOTA — {pet.name}", lines, style="cyan")
        print()

    # Mensaje de error bonito
    def show_error(self, message: str) -> None:
        self.panel("ERROR", [message], style="red")

    # Mensaje informativo
    def show_info(self, title: str, message_lines: Sequence[str]) -> None:
        self.panel(title, list(message_lines), style="yellow")

# -------------------------
# DEMOSTRACIÓN DE USO
# -------------------------
if __name__ == "__main__":
    shelter = Shelter("Refugio Arcoíris 🐾")
    ui = PrettyUI(shelter)

    # Añadir mascotas ejemplo
    shelter.add_pet(Pet(name="Luna", species="Perro", breed="Labrador", age_years=3, vaccinated=True, neutered=True, notes="Muy cariñosa, ideal para familia."))
    shelter.add_pet(Pet(name="Misu", species="Gato", breed="Europeo", age_years=2, vaccinated=True, neutered=False, notes="Tranquilo y curioso."))
    shelter.add_pet(Pet(name="Copito", species="Conejo", breed="Enano", age_years=1, vaccinated=False, neutered=False, notes="Requiere jaula amplia."))

    # Registrar adoptantes
    maria = Adopter(name="María Pérez", contact="maria@example.com")
    juan = Adopter(name="Juan López", contact="juan@example.com")
    shelter.register_adopter(maria)
    shelter.register_adopter(juan)

    # Mostrar interfaz inicial
    ui.header("Sistema de Adopción — Refugio Arcoíris")
    ui.show_summary()
    ui.show_pets(only_available=True)
    ui.show_adopters()
    ui.show_applications()

    # Flujo: María aplica por Luna
    luna_id = next(p.pet_id for p in shelter.pets.values() if p.name == "Luna")
    try:
        app1 = shelter.create_application(adopter_id=maria.adopter_id, pet_id=luna_id, message="Tengo patio y experiencia con perros.")
        ui.show_info("Solicitud creada", [f"ID: {app1.application_id}", f"Adoptante: {maria.name}", f"Mascota: Luna ({luna_id})"])
    except Exception as e:
        ui.show_error(str(e))

    ui.show_applications()

    # Revisar y aprobar
    try:
        shelter.review_application(app1.application_id, action="under_review", reviewer="Ana (voluntaria)")
        shelter.review_application(app1.application_id, action="approve", reviewer="Pedro (coordinador)")
        ui.show_info("Solicitud aprobada", [f"Solicitud {app1.application_id} aprobada por {app1.reviewed_by}"])
    except Exception as e:
        ui.show_error(str(e))

    ui.show_applications()

    # Finalizar adopción
    try:
        shelter.finalize_adoption(app1.application_id)
        ui.show_info("Adopción finalizada", [f"{maria.name} ha adoptado a Luna. ¡Felicidades!"])
    except Exception as e:
        ui.show_error(str(e))

    ui.show_pets(only_available=False)
    ui.show_applications()
    ui.pet_card(luna_id)

    # Juan intenta aplicar por Luna (debe fallar)
    try:
        shelter.create_application(adopter_id=juan.adopter_id, pet_id=luna_id)
    except Exception as e:
        ui.show_error(f"Intento de Juan falló: {e}")

    # Juan aplica por Copito
    copito_id = next(p.pet_id for p in shelter.pets.values() if p.name == "Copito")
    try:
        app2 = shelter.create_application(adopter_id=juan.adopter_id, pet_id=copito_id, message="Busco un compañero tranquilo.")
        ui.show_info("Solicitud creada", [f"ID: {app2.application_id}", f"Adoptante: {juan.name}", f"Mascota: Copito ({copito_id})"])
    except Exception as e:
        ui.show_error(str(e))

    ui.show_applications()

    # Rechazar la solicitud de Juan (ejemplo)
    try:
        shelter.review_application(app2.application_id, action="reject", reviewer="Coordinador", reason="Vivienda no adecuada para conejo.")
        ui.show_info("Solicitud rechazada", [f"Solicitud {app2.application_id} rechazada. Copito vuelve a disponible."])
    except Exception as e:
        ui.show_error(str(e))

    ui.show_pets(only_available=True)
    ui.show_applications()

    # Resumen final
    ui.header("Resumen final del refugio")
    ui.show_summary()
    print()  # línea final