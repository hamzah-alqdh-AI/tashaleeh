import sqlite3
from contextlib import closing

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
    """
    INSERT INTO makes (name)
    VALUES (?)
    ON CONFLICT (name) DO NOTHING
    """,
    makes,
)


def seed_models(connection):
    models = [
        ("Toyota", "Camry"),
        ("Toyota", "Land Cruiser"),
        ("Toyota", "Hilux"),
        ("Toyota", "Corolla"),
        ("Lexus", "LX"),
        ("Lexus", "ES"),
        ("Nissan", "Patrol"),
        ("Hyundai", "Sonata"),
    ]
    connection.executemany(
    """
    INSERT INTO models (make_id, name)
    VALUES ((SELECT id FROM makes WHERE name = ?), ?)
    ON CONFLICT (make_id, name) DO NOTHING
    """,
    models,
)


def fetch_all_makes():
    with closing(get_connection()) as connection:
        rows = connection.execute(
            """
            SELECT id, name
            FROM makes
            ORDER BY name
            """
        ).fetchall()
    return [{"id": make_id, "name": make_name} for make_id, make_name in rows]

def fetch_models_by_make(make_id):
    with closing(get_connection()) as connection:
        rows = connection.execute(
            """
            SELECT id, name FROM models
            WHERE make_id = ?
            ORDER BY name
            """,
            (make_id,),
        ).fetchall()
    return [{"id": model_id, "name": model_name} for model_id, model_name in rows]

def main():
    with closing(get_connection()) as connection:
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



if __name__ == "__main__":
    main()