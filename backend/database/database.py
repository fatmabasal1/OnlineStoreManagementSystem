import sqlite3

DATABASE_NAME = "store.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            category TEXT,
            image_url TEXT,
            rating REAL DEFAULT 0
        )
    """)

    columns = connection.execute(
        "PRAGMA table_info(products)"
    ).fetchall()

    column_names = [column["name"] for column in columns]

    if "image_url" not in column_names:
        connection.execute(
            "ALTER TABLE products ADD COLUMN image_url TEXT"
        )

    if "rating" not in column_names:
        connection.execute(
            "ALTER TABLE products ADD COLUMN rating REAL DEFAULT 0"
        )

    connection.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()