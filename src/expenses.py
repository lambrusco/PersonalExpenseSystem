"""Modulo 2 — Inserimento di una Spesa"""

import sqlite3
from datetime import datetime

from utils import lookup_category_id, parse_amount


def expenses_menu(conn: sqlite3.Connection) -> None:
    """Raccoglie i dati da tastiera e inserisce una spesa.

    Ripete la richiesta se l'input non è valido.
    """
    print("--- INSERIMENTO SPESA ---")

    while True:
        raw_date = input("Data (YYYY-MM-DD): ").strip()
        expense_date = _parse_date(raw_date)
        if expense_date is not None:
            break
        print("Errore: data non valida. Formato richiesto: YYYY-MM-DD.")

    while True:
        raw_amount = input("Importo: ").strip()
        amount = parse_amount(raw_amount)
        if amount is None:
            print("Errore: importo non valido.")
            continue
        if amount <= 0:
            print("Errore: l'importo deve essere maggiore di zero.")
            continue
        break

    while True:
        raw_category = input("Categoria: ").strip()
        if not raw_category:
            print("Errore: il nome della categoria non può essere vuoto.")
            continue
        category_id = lookup_category_id(conn, raw_category)
        if category_id is not None:
            break
        print("Errore: la categoria non esiste.")

    description = input("Descrizione (facoltativa): ").strip() or None

    try:
        conn.execute(
            "INSERT INTO expenses(expense_date, amount, category_id, description) "
            "VALUES (?, ?, ?, ?)",
            (expense_date, str(amount), category_id, description),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("Errore: impossibile inserire la spesa.")
        print(str(e))
        return

    print("Spesa inserita correttamente.")


def _parse_date(raw: str) -> str | None:
    """Valida una data YYYY-MM-DD. Restituisce la stringa normalizzata o None."""
    try:
        dt = datetime.strptime(raw, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None
