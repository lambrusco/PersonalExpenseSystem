"""Modulo di supporto 2 — Funzioni condivise"""

import sqlite3
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation


def parse_amount(raw: str) -> Decimal | None:
    """Analizza un importo accettando sia . che , come separatore decimale.

    Restituisce None se il valore non è valido.
    """
    normalized = raw.replace(",", ".")
    try:
        value = Decimal(normalized)
    except InvalidOperation:
        return None
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def to_decimal(value) -> Decimal:
    """Converte un valore numerico SQLite in Decimal."""
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def lookup_category_id(conn: sqlite3.Connection, name: str) -> int | None:
    """Cerca l'ID di una categoria per nome. Restituisce None se non trovata."""
    cursor = conn.execute("SELECT id FROM categories WHERE name = ?", (name,))
    row = cursor.fetchone()
    return row["id"] if row else None
