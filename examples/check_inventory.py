"""Reproduce the sample resume's results with synthetic data in SQLite."""

import sqlite3

ROW_COUNT = 10_000
BATCH_SIZE = 500


def open_database():
    database = sqlite3.connect(":memory:")
    database.executescript("""
        CREATE TABLE catalog (sku INTEGER PRIMARY KEY);
        CREATE TABLE imported_batch (code TEXT PRIMARY KEY);
        CREATE TABLE stock (sku INTEGER PRIMARY KEY, quantity INTEGER NOT NULL);
    """)
    with database:
        database.executemany("INSERT INTO catalog VALUES (?)",
                             ((sku,) for sku in range(1, ROW_COUNT + 1)))
    return database


def import_rows(database, batch, rows, query_batch_size):
    with database:
        claimed = database.execute(
            "INSERT OR IGNORE INTO imported_batch VALUES (?)", (batch,)
        ).rowcount
        if not claimed:
            return False
        for start in range(0, len(rows), query_batch_size):
            group = rows[start:start + query_batch_size]
            slots = ", ".join("?" for _ in group)
            known = {row[0] for row in database.execute(
                f"SELECT sku FROM catalog WHERE sku IN ({slots})",
                [sku for sku, _ in group],
            )}
            for sku, quantity in group:
                if sku not in known or quantity <= 0:
                    raise ValueError(f"Invalid row for SKU {sku}")
                database.execute("""
                    INSERT INTO stock VALUES (?, ?)
                    ON CONFLICT(sku) DO UPDATE SET quantity = quantity + excluded.quantity
                """, (sku, quantity))
    return True


def run_comparison(database, rows, query_batch_size):
    catalog_queries = 0

    def trace(statement):
        nonlocal catalog_queries
        if statement.startswith("SELECT sku FROM catalog WHERE"):
            catalog_queries += 1

    database.set_trace_callback(trace)
    try:
        applied = import_rows(database, "comparison", rows, query_batch_size)
        assert applied
    finally:
        database.set_trace_callback(None)
    return catalog_queries


def read_inventory(database):
    return database.execute("SELECT sku, quantity FROM stock ORDER BY sku").fetchall()


def main():
    rows = [(sku, 1) for sku in range(1, ROW_COUNT + 1)]
    per_row, batched = open_database(), open_database()
    try:
        old_queries = run_comparison(per_row, rows, 1)
        new_queries = run_comparison(batched, rows, BATCH_SIZE)
        assert (old_queries, new_queries) == (ROW_COUNT, 20)
        assert read_inventory(per_row) == read_inventory(batched) == rows

        # The second row fails after the first change is already in the transaction.
        try:
            import_rows(batched, "retry", [(1, 4), (2, 0)], BATCH_SIZE)
        except ValueError:
            assert read_inventory(batched) == rows
        else:
            raise AssertionError("Invalid row was accepted")

        corrected = [(1, 4), (2, 1)]
        applied = import_rows(batched, "retry", corrected, BATCH_SIZE)
        assert applied
        assert read_inventory(batched)[:2] == [(1, 5), (2, 2)]
        applied = import_rows(batched, "retry", corrected, BATCH_SIZE)
        assert not applied
        assert read_inventory(batched)[:2] == [(1, 5), (2, 2)]
    finally:
        per_row.close()
        batched.close()

    print(f"SQLite in-memory fixture: {ROW_COUNT:,} synthetic rows")
    print(f"Catalog SELECTs: {old_queries:,} -> {new_queries} ({BATCH_SIZE} rows per query)")
    print("Inventory results match; invalid-row rollback, corrected retry and duplicate submission passed.")


if __name__ == "__main__":
    main()
