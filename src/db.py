"""Modulo di supporto 1 — Gestione database"""

import sqlite3
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SCHEMA_PATH = _PROJECT_ROOT / "sql" / "schema.sql"
_SEED_DATA_PATH = _PROJECT_ROOT / "sql" / "seed_data.sql"


def get_connection(db_path: Path) -> sqlite3.Connection:
    """Apre una connessione SQLite con chiavi esterne abilitate e Row factory."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path, with_seed_data: bool = False) -> None:
    """Inizializza lo schema del database, e i dati demo se with_seed_data=True."""
    if not _SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"File dello schema del db non presente: {_SCHEMA_PATH}"
        )

    conn = get_connection(db_path)
    try:
        schema_content = _SCHEMA_PATH.read_text()
        conn.executescript(schema_content)

        if with_seed_data:
            if not _SEED_DATA_PATH.exists():
                raise FileNotFoundError(
                    f"File di seed dei dati non presente: {_SEED_DATA_PATH}"
                )
            seed_content = _SEED_DATA_PATH.read_text()
            conn.executescript(seed_content)

        conn.commit()
    finally:
        conn.close()
