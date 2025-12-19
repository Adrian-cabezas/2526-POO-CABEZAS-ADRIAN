"""
Sistema de gestión de biblioteca (POO) con salida estética en consola.

Este archivo reutiliza las mismas clases de dominio (Book, Member, Loan, Library)
pero añade utilidades de impresión (PrettyPrinter) para mostrar catálogos, socios
y préstamos de forma tabular y visualmente agradable en la terminal.

Notas:
- No requiere dependencias externas (solo biblioteca estándar).
- Usa caracteres Unicode para cajas/tablas; si su terminal no soporta Unicode,
  los cuadros pueden verse menos precisos pero el contenido seguirá siendo legible.
- Incluye resaltado con colores ANSI; si su terminal no los soporta, puede ignorarlos.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Sequence
import uuid


# ------------------------------
# Clases de dominio (POO)
# ------------------------------
@dataclass
class Book:
    isbn: str
    title: str
    author: str
    total_copies: int = 1
    available_copies: int = 1

    def __post_init__(self):
        if self.available_copies > self.total_copies:
            self.available_copies = self.total_copies

    def add_copies(self, count: int = 1) -> None:
        if count < 1:
            raise ValueError("count debe ser >= 1")
        self.total_copies += count
        self.available_copies += count

    def remove_copies(self, count: int = 1) -> None:
        if count < 1:
            raise ValueError("count debe ser >= 1")
        if count > self.available_copies:
            raise ValueError("No se pueden eliminar copias que están prestadas")
        if count > self.total_copies:
            raise ValueError("No hay tantas copias para remover")
        self.total_copies -= count
        self.available_copies -= count

    def is_available(self) -> bool:
        return self.available_copies > 0


@dataclass
class Member:
    name: str
    member_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    max_loans: int = 3


@dataclass
class Loan:
    book_isbn: str
    member_id: str
    loan_date: datetime = field(default_factory=datetime.now)
    due_date: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=14))
    loan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    returned_date: Optional[datetime] = None

    def mark_returned(self, when: Optional[datetime] = None) -> None:
        self.returned_date = when or datetime.now()

    def is_overdue(self, on_date: Optional[datetime] = None) -> bool:
        if self.returned_date:
            return False
        now = on_date or datetime.now()
        return now > self.due_date

    def status(self) -> str:
        if self.returned_date:
            return "Devuelto"
        if self.is_overdue():
            return "Vencido"
        return "En préstamo"


class Library:
    def __init__(self, name: str):
        self.name = name
        self.catalog: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.loans: Dict[str, Loan] = {}

    # Gestión de libros
    def add_book(self, book: Book) -> None:
        if book.isbn in self.catalog:
            existing = self.catalog[book.isbn]
            existing.add_copies(book.total_copies)
        else:
            self.catalog[book.isbn] = book

    def remove_book(self, isbn: str, count: int = 1) -> None:
        if isbn not in self.catalog:
            raise KeyError("ISBN no encontrado en el catálogo")
        book = self.catalog[isbn]
        book.remove_copies(count)
        if book.total_copies == 0:
            del self.catalog[isbn]

    def search_books(self, query: str) -> List[Book]:
        q = query.lower()
        return [b for b in self.catalog.values() if q in b.title.lower() or q in b.author.lower() or q in b.isbn.lower()]

    def list_available_books(self) -> List[Book]:
        return [b for b in self.catalog.values() if b.is_available()]

    # Gestión de socios
    def register_member(self, member: Member) -> None:
        if member.member_id in self.members:
            raise KeyError("Miembro ya registrado")
        self.members[member.member_id] = member

    def remove_member(self, member_id: str) -> None:
        active = [loan for loan in self.loans.values() if loan.member_id == member_id and not loan.returned_date]
        if active:
            raise ValueError("El miembro tiene préstamos activos y no puede ser eliminado")
        if member_id in self.members:
            del self.members[member_id]
        else:
            raise KeyError("Miembro no encontrado")

    def get_member_loans(self, member_id: str) -> List[Loan]:
        return [loan for loan in self.loans.values() if loan.member_id == member_id]

    # Préstamos
    def borrow_book(self, member_id: str, isbn: str, days: int = 14) -> Loan:
        if member_id not in self.members:
            raise KeyError("Miembro no registrado")
        if isbn not in self.catalog:
            raise KeyError("ISBN no encontrado")
        member = self.members[member_id]
        book = self.catalog[isbn]

        active_loans = [loan for loan in self.loans.values() if loan.member_id == member_id and not loan.returned_date]
        if len(active_loans) >= member.max_loans:
            raise ValueError("El miembro ha alcanzado el número máximo de préstamos activos")
        if not book.is_available():
            raise ValueError("No hay copias disponibles para préstamo")

        loan = Loan(book_isbn=isbn, member_id=member_id, loan_date=datetime.now(), due_date=datetime.now() + timedelta(days=days))
        self.loans[loan.loan_id] = loan
        book.available_copies -= 1
        return loan

    def return_book(self, loan_id: str) -> None:
        if loan_id not in self.loans:
            raise KeyError("Préstamo no encontrado")
        loan = self.loans[loan_id]
        if loan.returned_date:
            raise ValueError("El préstamo ya fue devuelto")
        loan.mark_returned()
        isbn = loan.book_isbn
        if isbn in self.catalog:
            self.catalog[isbn].available_copies += 1
        else:
            self.catalog[isbn] = Book(isbn=isbn, title="Título desconocido", author="Autor desconocido", total_copies=1, available_copies=1)

    def list_overdue_loans(self, on_date: Optional[datetime] = None) -> List[Loan]:
        return [loan for loan in self.loans.values() if loan.is_overdue(on_date)]

    def __str__(self) -> str:
        return f"{self.name} — {len(self.catalog)} libros, {len(self.members)} socios, {len(self.loans)} préstamos"


# ------------------------------
# Utilidades de impresión estética
# ------------------------------
class PrettyPrinter:
    """
    Imprime tablas y secciones con estilo en la terminal.

    Métodos principales:
    - header: título grande
    - table: tabla genérica (cabeceras + filas)
    - print_catalog, print_members, print_loans, print_overdue: funciones específicas
    """

    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "cyan": "\033[36m",
    }

    def __init__(self, use_color: bool = True):
        self.use_color = use_color and self._terminal_supports_color()

    def _color(self, text: str, color: str) -> str:
        if not self.use_color or color not in self.COLORS:
            return text
        return f"{self.COLORS[color]}{text}{self.COLORS['reset']}"

    def header(self, title: str) -> None:
        line = "═" * (len(title) + 4)
        print(self._color("╔" + line + "╗", "cyan"))
        print(self._color(f"║  {title}  ║", "cyan"))
        print(self._color("╚" + line + "╝", "cyan"))

    def table(self, headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> None:
        # Calcular anchos de columnas
        cols = len(headers)
        col_widths = [len(h) for h in headers]
        for r in rows:
            for i in range(cols):
                val = "" if i >= len(r) or r[i] is None else str(r[i])
                col_widths[i] = max(col_widths[i], len(val))
        # Construir líneas
        sep = "─"
        top = "┌" + "┬".join(sep * (w + 2) for w in col_widths) + "┐"
        mid = "├" + "┼".join(sep * (w + 2) for w in col_widths) + "┤"
        bot = "└" + "┴".join(sep * (w + 2) for w in col_widths) + "┘"
        print(top)
        # Headers
        header_cells = []
        for i, h in enumerate(headers):
            header_cells.append(" " + h.ljust(col_widths[i]) + " ")
        print("│" + "│".join(self._color(c, "bold") for c in header_cells) + "│")
        print(mid)
        # Filas
        for row in rows:
            cells = []
            for i in range(cols):
                val = "" if i >= len(row) or row[i] is None else str(row[i])
                cells.append(" " + val.ljust(col_widths[i]) + " ")
            print("│" + "│".join(cells) + "│")
        print(bot)

    def print_catalog(self, catalog: Dict[str, Book]) -> None:
        self.header("Catálogo de libros")
        headers = ["ISBN", "Título", "Autor", "Disp/Total"]
        rows = []
        for b in catalog.values():
            rows.append([b.isbn, b.title, b.author, f"{b.available_copies}/{b.total_copies}"])
        if rows:
            self.table(headers, rows)
        else:
            print(self._color("No hay libros en el catálogo.", "yellow"))
        print()

    def print_members(self, members: Dict[str, Member], library: Library) -> None:
        self.header("Socios registrados")
        headers = ["ID", "Nombre", "Máx préstamos", "Préstamos activos"]
        rows = []
        for m in members.values():
            active = len([l for l in library.loans.values() if l.member_id == m.member_id and not l.returned_date])
            rows.append([m.member_id, m.name, m.max_loans, active])
        if rows:
            self.table(headers, rows)
        else:
            print(self._color("No hay socios registrados.", "yellow"))
        print()

    def print_loans(self, loans: Dict[str, Loan], library: Library, show_all: bool = True) -> None:
        title = "Préstamos (todos)" if show_all else "Préstamos activos"
        self.header(title)
        headers = ["Loan ID", "ISBN", "Título", "Miembro", "Prestado", "Vence", "Estado"]
        rows = []
        for loan in loans.values():
            if not show_all and loan.returned_date:
                continue
            book_title = library.catalog[loan.book_isbn].title if loan.book_isbn in library.catalog else "Desconocido"
            status = loan.status()
            # Resaltar vencidos en rojo y devueltos en verde
            if status == "Vencido":
                status = self._color(status, "red")
            elif status == "Devuelto":
                status = self._color(status, "green")
            rows.append([
                loan.loan_id,
                loan.book_isbn,
                book_title,
                loan.member_id,
                loan.loan_date.strftime("%Y-%m-%d"),
                loan.due_date.strftime("%Y-%m-%d"),
                status
            ])
        if rows:
            self.table(headers, rows)
        else:
            print(self._color("No hay préstamos para mostrar.", "yellow"))
        print()

    def print_overdue(self, loans: Dict[str, Loan], library: Library) -> None:
        self.header("Préstamos vencidos")
        overdue = [l for l in loans.values() if l.is_overdue()]
        if not overdue:
            print(self._color("No hay préstamos vencidos. ¡Bien hecho!", "green"))
            print()
            return
        headers = ["Loan ID", "ISBN", "Título", "Miembro", "Vence", "Días vencido"]
        rows = []
        today = datetime.now().date()
        for l in overdue:
            days = (today - l.due_date.date()).days
            rows.append([l.loan_id, l.book_isbn, library.catalog.get(l.book_isbn, Book(l.book_isbn, "Desconocido", "Desconocido")).title, l.member_id, l.due_date.strftime("%Y-%m-%d"), days])
        # Resaltar toda la tabla en amarillo/rojo si hay vencidos
        self.table(headers, rows)
        print(self._color(f"Total vencidos: {len(overdue)}", "red"))
        print()

    def _terminal_supports_color(self) -> bool:
        # Verificación simple: si stdout tiene isatty, asumimos soporte ANSI.
        try:
            import sys
            return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
        except Exception:
            return False


# ------------------------------
# Demostración con salida estética
# ------------------------------
if __name__ == "__main__":
    pp = PrettyPrinter(use_color=True)

    biblioteca = Library("Biblioteca Central")

    # Añadir ejemplos de libros
    biblioteca.add_book(Book(isbn="978-0140449136", title="La Odisea", author="Homero", total_copies=3, available_copies=3))
    biblioteca.add_book(Book(isbn="978-8496452830", title="Cien años de soledad", author="Gabriel García Márquez", total_copies=2, available_copies=2))
    biblioteca.add_book(Book(isbn="978-0307277671", title="El hombre en busca de sentido", author="Viktor E. Frankl", total_copies=1, available_copies=1))

    # Registrar socios
    alice = Member(name="Alice")
    bob = Member(name="Bob", max_loans=2)
    biblioteca.register_member(alice)
    biblioteca.register_member(bob)

    # Préstamos de ejemplo
    l1 = biblioteca.borrow_book(alice.member_id, "978-0140449136", days=21)
    l2 = biblioteca.borrow_book(bob.member_id, "978-8496452830", days=7)

    # Crear préstamo vencido manualmente
    old_loan = Loan(book_isbn="978-0307277671", member_id=bob.member_id, loan_date=datetime.now() - timedelta(days=40), due_date=datetime.now() - timedelta(days=26))
    biblioteca.loans[old_loan.loan_id] = old_loan
    biblioteca.catalog["978-0307277671"].available_copies -= 1

    # Mostrar pantallas bonitas
    pp.header(str(biblioteca))
    print()
    pp.print_catalog(biblioteca.catalog)
    pp.print_members(biblioteca.members, biblioteca)
    pp.print_loans(biblioteca.loans, biblioteca, show_all=False)  # solo activos
    pp.print_overdue(biblioteca.loans, biblioteca)

    # Devolvemos un libro y mostramos cambios
    biblioteca.return_book(l1.loan_id)
    pp.header("Después de una devolución")
    pp.print_catalog(biblioteca.catalog)
    pp.print_loans(biblioteca.loans, biblioteca, show_all=False)