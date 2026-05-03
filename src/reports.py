"""Modulo 4 — Visualizzazione dei Report"""

import sqlite3

from utils import to_decimal


def reports_menu(conn: sqlite3.Connection) -> None:
    """Menu dei report: totali per categoria, mensili vs budget, elenco spese."""

    while True:
        _print_menu()
        choice = input("Inserisci la tua scelta: ").strip()

        if not choice:
            print("Scelta non valida. Riprovare.")
            continue

        match choice:
            case "1":
                _report_totals_by_category(conn)
            case "2":
                _report_monthly_vs_budget(conn)
            case "3":
                _report_all_expenses(conn)
            case "4":
                return
            case _:
                print("Scelta non valida. Riprovare.")


def _print_menu() -> None:
    """Stampa il sotto-menu dei report."""
    print()
    print("--- REPORT ---")
    print("1. Totale spese per categoria")
    print("2. Spese mensili vs budget")
    print("3. Elenco completo delle spese")
    print("4. Torna al menu principale")


def _report_totals_by_category(conn: sqlite3.Connection) -> None:
    """Stampa il totale delle spese per categoria, ordinate per totale decrescente.

    Usa COALESCE per sostituire NULL con 0.
    Usa LEFT JOIN in modo che le categorie senza spese appaiano comunque.
    """
    cursor = conn.execute(
        """
        SELECT c.name AS category, COALESCE(SUM(e.amount), 0) AS total
        FROM categories c
        LEFT JOIN expenses e ON e.category_id = c.id
        GROUP BY c.id, c.name
        ORDER BY total DESC, c.name ASC
        """
    )
    rows = cursor.fetchall()

    if not rows:
        print("Nessuna categoria presente.")
        return

    # Trovo la categoria più lunga per definire la lunghezza della colonna
    max_name_len = max(len(row["category"]) for row in rows)
    col_width = max(max_name_len, len("Categoria")) + 2

    print()
    print("--- TOTALE SPESE PER CATEGORIA ---")
    header = f"{'Categoria':<{col_width}}{'Totale Speso':>12}"
    print(header)
    print("-" * len(header))

    for row in rows:
        total = to_decimal(row["total"])
        print(f"{row['category']:<{col_width}}{total:>12.2f}")


def _report_monthly_vs_budget(conn: sqlite3.Connection) -> None:
    """Stampa le spese mensili vs budget per categoria

    Usa LEFT JOIN e COALESCE sulle spese così i budget senza spese mostrano speso=0.00.
    """
    cursor = conn.execute(
        """
        SELECT
            b.month,
            c.name AS category,
            b.amount AS budget,
            COALESCE(SUM(e.amount), 0) AS spent
        FROM budgets b
        JOIN categories c ON c.id = b.category_id
        LEFT JOIN expenses e
            ON e.category_id = b.category_id
            AND substr(e.expense_date, 1, 7) = b.month
        GROUP BY b.id, b.month, c.name, b.amount
        ORDER BY b.month ASC, c.name ASC
        """
    )
    rows = cursor.fetchall()

    if not rows:
        print("Nessun budget definito.")
        return

    print()
    print("--- SPESE MENSILI VS BUDGET ---")

    for row in rows:
        budget = to_decimal(row["budget"])
        spent = to_decimal(row["spent"])
        status = "SUPERAMENTO BUDGET" if spent > budget else "OK"

        print()
        print(f"Mese: {row['month']}")
        print(f"Categoria: {row['category']}")
        print(f"Budget: {budget:.2f}")
        print(f"Speso: {spent:.2f}")
        print(f"Stato: {status}")


def _report_all_expenses(conn: sqlite3.Connection) -> None:
    """Stampa tutte le spese in ordine cronologico."""

    cursor = conn.execute(
        """
        SELECT e.expense_date, c.name AS category, e.amount, e.description
        FROM expenses e
        JOIN categories c ON c.id = e.category_id
        ORDER BY e.expense_date ASC, e.id ASC
        """
    )
    rows = cursor.fetchall()

    if not rows:
        print("Nessuna spesa registrata.")
        return

    # Trovo la categoria più lunga per definire la lunghezza della colonna
    max_cat_len = max(len(row["category"]) for row in rows)
    cat_width = max(max_cat_len, len("Categoria")) + 2

    print()
    print("--- ELENCO COMPLETO DELLE SPESE ---")
    header = f"{'Data':<12}{'Categoria':<{cat_width}}{'Importo':>9}  Descrizione"
    print(header)
    print("-" * len(header))

    for row in rows:
        amount = to_decimal(row["amount"])
        print(
            f"{row['expense_date']:<12}{row['category']:<{cat_width}}"
            f"{amount:>9.2f}  {row['description'] or ''}"
        )
