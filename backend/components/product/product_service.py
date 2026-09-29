from database.database import get_connection


def create_product(name, description, price, stock, category):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO products (name, description, price, stock, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, description, price, stock, category)
    )

    connection.commit()
    product_id = cursor.lastrowid
    connection.close()

    return get_product(product_id)


def get_products():
    connection = get_connection()

    products = connection.execute(
        """
        SELECT * FROM products
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [dict(product) for product in products]


def get_product(product_id):
    connection = get_connection()

    product = connection.execute(
        """
        SELECT * FROM products
        WHERE id = ?
        """,
        (product_id,)
    ).fetchone()

    connection.close()

    if product is None:
        return None

    return dict(product)


def update_product(product_id, name, description, price, stock, category):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE products
        SET name = ?, description = ?, price = ?, stock = ?, category = ?
        WHERE id = ?
        """,
        (name, description, price, stock, category, product_id)
    )

    connection.commit()
    updated = cursor.rowcount
    connection.close()

    if updated == 0:
        return None

    return get_product(product_id)


def delete_product(product_id):
    connection = get_connection()

    cursor = connection.execute(
        """
        DELETE FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    connection.commit()
    deleted = cursor.rowcount
    connection.close()

    return deleted > 0