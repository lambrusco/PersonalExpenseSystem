-- PersonalExpenseSystem — Database Schema
-- La creazione di tabelle e indici è idempotente (utilizzo di IF NOT EXISTS)


-- Tabella: categories
-- Vincoli di integrità:
--   Vincolo di unicità del campo name
CREATE TABLE IF NOT EXISTS categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT    NOT NULL UNIQUE CHECK (length(trim(name)) > 0)
);

-- Tabella: expenses
-- Vincoli di integrità:
--   Vincolo referenziale con la tabella categories
--   Vincolo sul valore di amount > 0
--   Vincolo sul formato di expense_date (AAAA-MM-DD)
CREATE TABLE IF NOT EXISTS expenses (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_date TEXT    NOT NULL CHECK (expense_date LIKE '____-__-__'),
    amount       NUMERIC NOT NULL CHECK (amount > 0),
    category_id  INTEGER NOT NULL,
    description  TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Table: budgets
-- Vincoli di integrità:
--   Vincolo di integrità referenziale con la tabella categories
--   Vincolo sul valore di amount > 0
--   Vincolo sul formato di month (AAAA-MM)
--   Vincolo di unicità composito (month e category_id)
CREATE TABLE IF NOT EXISTS budgets (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    month       TEXT    NOT NULL CHECK (month LIKE '____-__'),
    category_id INTEGER NOT NULL,
    amount      NUMERIC NOT NULL CHECK (amount > 0),
    UNIQUE (month, category_id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Indici per i report
CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category_id);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(expense_date);
