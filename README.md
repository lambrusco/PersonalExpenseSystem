# Personal Expense System

Sistema di gestione delle spese personali e del budget basato su console (CLI), sviluppato in Python con database SQLite.

## Indice

- [Descrizione del progetto](#descrizione-del-progetto)
- [Requisiti](#requisiti)
- [Struttura del repository](#struttura-del-repository)
- [Installazione](#installazione)
- [Esecuzione del programma](#esecuzione-del-programma)
- [Funzionalità](#funzionalità)
- [Schema del database](#schema-del-database)


## Descrizione del progetto

Progetto per il corso di Fondamenti di Informatica, L-8 Ingegneria Informatica, Università Telematica San Raffaele, anno accademico 2025/2026.

Applicazione CLI per la gestione delle spese personali e dei budget mensili per utente singolo.

Permette di categorizzare le uscite, definire tetti di spesa mensili per categoria e visualizzare report di sintesi.


## Requisiti

- **Python 3.13 o superiore**
- **sqlite3** (incluso nella libreria standard di Python)

## Struttura del repository

```text
/
├── src/
│   ├── main.py           # Entry point: inizializzazione, menu principale, ciclo di navigazione
│   ├── categories.py     # Modulo 1 — Gestione categorie
│   ├── expenses.py       # Modulo 2 — Inserimento spese
│   ├── budgets.py        # Modulo 3 — Definizione budget mensili
│   └── reports.py        # Modulo 4 — Visualizzazione report
│   ├── db.py             # Connessione SQLite e inizializzazione dello schema
│   ├── utils.py          # Funzioni condivise
├── sql/
│   ├── schema.sql        # DDL: tabelle, vincoli e indici
│   ├── seed_data.sql     # Dati di esempio per demo
│   └── schema.md         # Diagramma logico del database
├── demo/
│   └── demo_video.mp4    # Video dimostrativo
├── data/
│   └── expenses.db       # File SQLite (creato a runtime, ignorato da git)
├── README.md
```

* `src/` contiene i quattro moduli applicativi e il database layer.
* `sql/` contiene lo schema DDL e i dati di esempio.

## Installazione

```bash
git clone https://github.com/lambrusco/PersonalExpenseSystem.git
cd PersonalExpenseSystem
```

## Esecuzione del programma
```bash
python src/main.py
```

Se `expenses.db` non esiste viene creato automaticamente con lo schema vuoto nella cartella `data`.


### Inizializzazione del database

```bash
python src/main.py --init
```

- Cancella `expenses.db` e ricrea lo schema vuoto.
- Esegue il programma


### Inizializzazione con dati di esempio
```bash
python src/main.py --init --with-seed-data
```

- Cancella `expenses.db` e ricrea lo schema vuoto.
- Popola il database con categorie, spese e budget di esempio.
- Esegue il programma.

## Schema del database

Il database è composto da tre tabelle.
* `categories` registra le categorie di spesa con nome univoco.
* `expenses` memorizza ogni spesa con data, importo e riferimento alla categoria tramite chiave esterna.
* `budgets` associa un importo massimo mensile a una categoria, con il vincolo di unicità sulla coppia `(month, category_id)`.

Il diagramma logico si trova in [sql/schema.md](sql/schema.md).
