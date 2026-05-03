"""Script principale:
- Inizializzazione database
- Messaggio di benvenuto
- Visualizzazione del menu
- Lettura input utente ed esecuzione del modulo corrispondente
"""

import sys
from pathlib import Path

from budgets import budgets_menu
from categories import categories_menu
from db import get_connection, init_db
from expenses import expenses_menu
from reports import reports_menu

# Variabile globale che contiene la path del database
DB_PATH = Path(__file__).resolve().parent.parent / "data/expenses.db"


def main() -> None:
    """Gestione argomenti passati da CLI, mostra benvenuto e avvia menu principale."""

    # Controlla gli argomenti passati per verificare se e' richiesta l'inizializzazione
    args = sys.argv[1:]
    if "--init" in args:
        with_seed_data = "--with-seed-data" in args
        _handle_init(with_seed_data=with_seed_data)

    # Se il db non esiste inizializza lo schema automaticamente
    if not DB_PATH.exists():
        init_db(DB_PATH)

    print("Benvenuto nel Sistema di Gestione delle Spese Personali.")

    conn = get_connection(DB_PATH)
    try:
        running = True
        while running:
            _print_main_menu()
            choice = input("Inserisci la tua scelta: ").strip()

            match choice:
                case "1":
                    categories_menu(conn)
                case "2":
                    expenses_menu(conn)
                case "3":
                    budgets_menu(conn)
                case "4":
                    reports_menu(conn)
                case "5":
                    running = False
                case _:
                    print("Scelta non valida. Riprovare.")
    except KeyboardInterrupt:
        # Se l'utente preme Ctrl-C esci
        print()
    finally:
        # Chiudi la connessione prima di uscire
        conn.close()


def _handle_init(with_seed_data: bool = False) -> None:
    """Elimina il DB esistente e ricrea lo schema, con dati demo se richiesti."""

    # Elimina il database esistente
    DB_PATH.unlink(missing_ok=True)

    # Inizializza il database
    init_db(DB_PATH, with_seed_data=with_seed_data)
    if with_seed_data:
        print(f"Database inizializzato in {DB_PATH} con dati di esempio.")
    else:
        print(f"Database inizializzato in {DB_PATH}.")


def _print_main_menu() -> None:
    """Mostra il menu principale"""

    print()
    print("-------------------------")
    print("SISTEMA SPESE PERSONALI")
    print("-------------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("-------------------------")


# Esegui la funzione main quando invocato
if __name__ == "__main__":
    main()
