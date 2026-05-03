-- PersonalExpenseSystem — Demo Seed Data
--
-- Questo script va eseguito dopo aver inizializzato lo schema (schema.sql)
-- Tutti gli inserimenti sono effettuati in un unica transazione per garantirne la consistenza.
-- Gli id delle categorie sono referenziati usando delle subquery.

BEGIN;

-- Inserimento categorie
INSERT INTO categories(name) VALUES ('Alimentari');
INSERT INTO categories(name) VALUES ('Trasporti');
INSERT INTO categories(name) VALUES ('Casa');
INSERT INTO categories(name) VALUES ('Svago');
INSERT INTO categories(name) VALUES ('Salute');

-- Inserimento spese (28 totali su 3 mesi)
-- 2026-04: Alimentari (6 spese, totale 350, eccedente il budget di 300)
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-04-05', 55.20, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Spesa supermercato');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-04-08', 62.80, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Spesa settimanale');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-04-12', 60.60, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Frutta e verdura');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-04-18', 75.40, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Spesa supermercato');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-04-22', 62.00, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Alimentari vari');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-04-28', 34.00, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Pane e latticini');

-- 2026-04: Trasporti (4 spese, total 120, inferiore al budget di 150)
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-04-06', 28.50, (SELECT id FROM categories WHERE name = 'Trasporti'), 'Abbonamento metro');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-04-10', 32.00, (SELECT id FROM categories WHERE name = 'Trasporti'), 'Biglietto treno');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-04-15', 37.00, (SELECT id FROM categories WHERE name = 'Trasporti'), 'Benzina');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-04-25', 22.50, (SELECT id FROM categories WHERE name = 'Trasporti'), 'Abbonamento autobus');

-- 2026-03: Alimentari (5 spese, totale 264, inferiore al budget di 300)
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-03-03', 48.50, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Spesa supermercato');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-03-07', 55.00, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Spesa settimanale');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-03-11', 52.30, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Frutta e verdura');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-03-19', 65.20, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Spesa supermercato');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-03-25', 42.50, (SELECT id FROM categories WHERE name = 'Alimentari'), 'Alimentari vari');

-- 2026-03: Svago (2 spese, totale 100.50, eccedente il budget di 60)
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-03-05', 48.50, (SELECT id FROM categories WHERE name = 'Svago'), 'Cinema');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-03-18', 52.00, (SELECT id FROM categories WHERE name = 'Svago'), 'Ristorante');

-- 2026-02: Casa (3 spese, totale 212.50, inferiore al budget di 250)
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-02-02', 95.00, (SELECT id FROM categories WHERE name = 'Casa'), 'Manutenzione casa');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-02-08', 82.00, (SELECT id FROM categories WHERE name = 'Casa'), 'Materiali vari');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-02-20', 35.50, (SELECT id FROM categories WHERE name = 'Casa'), 'Attrezzi');

-- 2026-02: Salute (2 spese, total 83.50, eccedente il budget di 50)
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-02-10', 45.00, (SELECT id FROM categories WHERE name = 'Salute'), 'Farmacia');
INSERT INTO expenses(expense_date, amount, category_id, description)
  VALUES ('2026-02-25', 38.50, (SELECT id FROM categories WHERE name = 'Salute'), 'Visita medica');

-- Inserimento dei budget
INSERT INTO budgets(month, amount, category_id)
  VALUES ('2026-04', 300.00, (SELECT id FROM categories WHERE name = 'Alimentari'));
INSERT INTO budgets(month, amount, category_id)
  VALUES ('2026-04', 150.00, (SELECT id FROM categories WHERE name = 'Trasporti'));
INSERT INTO budgets(month, amount, category_id)
  VALUES ('2026-03', 300.00, (SELECT id FROM categories WHERE name = 'Alimentari'));
INSERT INTO budgets(month, amount, category_id)
  VALUES ('2026-03', 60.00, (SELECT id FROM categories WHERE name = 'Svago'));
INSERT INTO budgets(month, amount, category_id)
  VALUES ('2026-02', 250.00, (SELECT id FROM categories WHERE name = 'Casa'));
INSERT INTO budgets(month, amount, category_id)
  VALUES ('2026-02', 50.00, (SELECT id FROM categories WHERE name = 'Salute'));

COMMIT;
