import sqlite3

DATABASE_PATH = "tashaleeh.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_makes_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS makes (
            id   INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)


def create_models_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS models (
            id      INTEGER PRIMARY KEY,
            make_id INTEGER NOT NULL REFERENCES makes(id),
            name    TEXT NOT NULL,
            UNIQUE (make_id, name)
        )
    """)


def seed_makes(connection):
    makes = [("Toyota",), ("Lexus",), ("Nissan",), ("Hyundai",)]
    connection.executemany(
        "INSERT OR IGNORE INTO makes (name) VALUES (?)",
        makes,
    )


def seed_models(connection):
    models = [
        ("Toyota", "Camry"),
        ("Toyota", "Land Cruiser"),
        ("Toyota", "Hilux"),
        ("Lexus", "LX"),
        ("Lexus", "ES"),
        ("Nissan", "Patrol"),
        ("Hyundai", "Sonata"),
    ]
    connection.executemany(
        """
        INSERT OR IGNORE INTO models (make_id, name)
        VALUES ((SELECT id FROM makes WHERE name = ?), ?)
        """,
        models,
    )


def fetch_all_makes():
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT id, name 
        FROM makes
        ORDER BY name
        """
        ).fetchall()
    connection.close()
    return [{"id": make_id, "name": make_name} for make_id, make_name in rows]

def fetch_models_by_make(make_id):
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT id, name FROM models
        WHERE make_id = ?
        ORDER BY name
        """,
        (make_id,),
    ).fetchall()
    connection.close()
    return [{"id": model_id, "name": model_name} for model_id, model_name in rows]

def main():
    connection = get_connection()
    create_makes_table(connection)
    create_models_table(connection)
    seed_makes(connection)
    seed_models(connection)
    connection.commit()

    rows = connection.execute("""
        SELECT models.id, makes.name, models.name
        FROM models
        JOIN makes ON makes.id = models.make_id
    """)
    for row in rows:
        print(row)

    connection.close()


if __name__ == "__main__":
    main()