"""Modulo 1 — Gestione delle Categorie"""

import sqlite3


def categories_menu(conn: sqlite3.Connection) -> None:
    """Menu di gestione delle categorie: elenca, aggiunge e torna al menu principale."""
    while True:
        _print_menu()
        choice = input("Inserisci la tua scelta: ").strip()

        if not choice:
            print("Scelta non valida. Riprovare.")
            continue

        match choice:
            case "1":
                _list_categories(conn)
            case "2":
                _add_category(conn)
            case "3":
                return
            case _:
                print("Scelta non valida. Riprovare.")


def _print_menu() -> None:
    """Stampa il sotto-menu di gestione delle categorie."""
    print()
    print("--- GESTIONE CATEGORIE ---")
    print("1. Elenca categorie")
    print("2. Aggiungi categoria")
    print("3. Torna al menu principale")


def _list_categories(conn: sqlite3.Connection) -> None:
    """Elenca tutte le categorie, ordinate per nome."""
    cursor = conn.execute("SELECT name FROM categories ORDER BY name")
    rows = cursor.fetchall()

    if not rows:
        print("Nessuna categoria presente.")
    else:
        print("Categorie disponibili:")
        for row in rows:
            print(f"  - {row['name']}")


def _add_category(conn: sqlite3.Connection) -> None:
    """Richiede il nome di una nuova categoria, lo valida e lo inserisce."""

    name = input("Nome categoria: ").strip()

    if not name:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    # Ritorna al menu se la categoria esiste già
    cursor = conn.execute("SELECT 1 FROM categories WHERE name = ? LIMIT 1", (name,))
    if cursor.fetchone():
        print("La categoria esiste già.")
        return

    # Inserisce la nuova categoria
    try:
        conn.execute("INSERT INTO categories(name) VALUES (?)", (name,))
        conn.commit()
        print("Categoria inserita correttamente.")
    except sqlite3.IntegrityError as error:
        print(f"Errore di integrità: {error}")
