import sqlite3

DATABASE_PATH = "tashaleeh.db"


def create_makes_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS makes (
            id   INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)


def seed_makes(connection):
    makes = [("Toyota",), ("Lexus",), ("Nissan",), ("Hyundai",)]
    connection.executemany(
        "INSERT OR IGNORE INTO makes (name) VALUES (?)",
        makes,
    )


def main():
    connection = sqlite3.connect(DATABASE_PATH)
    create_makes_table(connection)
    seed_makes(connection)
    connection.commit()

    for row in connection.execute("SELECT id, name FROM makes"):
        print(row)

    connection.close()

def fetch_all_makes():
    connection = sqlite3.connect(DATABASE_PATH)
    rows = connection.execute("SELECT id, name FROM makes").fetchall()
    connection.close()
    return [{"id": row[0], "name": row[1]} for row in rows]

if __name__ == "__main__":
    main()