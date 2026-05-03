"""Modulo 3 — Gestione del Budget Mensile"""

import sqlite3
from datetime import datetime

from utils import lookup_category_id, parse_amount


def budgets_menu(conn: sqlite3.Connection) -> None:
    """Raccoglie i dati da tastiera e salva un budget mensile.

    Fa un upsert: aggiorna il budget se già esiste per quel mese e categoria.
    """
    print("--- DEFINIZIONE BUDGET MENSILE ---")

    raw_month = input("Mese (YYYY-MM): ").strip()
    month = _parse_month(raw_month)
    if month is None:
        print("Errore: mese non valido. Formato richiesto: YYYY-MM.")
        return

    category_name = input("Categoria: ").strip()
    if not category_name:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    # Prende nel db l'id della categoria a partire dal nome
    category_id = lookup_category_id(conn, category_name)
    if category_id is None:
        print("Errore: la categoria non esiste.")
        return

    raw_amount = input("Importo del budget: ").strip()
    amount = parse_amount(raw_amount)
    if amount is None:
        print("Errore: importo non valido.")
        return
    if amount <= 0:
        print("Errore: l'importo del budget deve essere maggiore di zero.")
        return

    try:
        conn.execute(
            "INSERT INTO budgets(month, category_id, amount) "
            "VALUES (?, ?, ?) "
            "ON CONFLICT(month, category_id) DO UPDATE SET amount = excluded.amount",
            (month, category_id, float(amount)),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("Errore: impossibile salvare il budget.")
        print(str(e))
        return

    print("Budget mensile salvato correttamente.")


def _parse_month(raw: str) -> str | None:
    """Valida un mese YYYY-MM. Restituisce la stringa normalizzata o None."""
    try:
        dt = datetime.strptime(raw, "%Y-%m")
        return dt.strftime("%Y-%m")
    except ValueError:
        return None
