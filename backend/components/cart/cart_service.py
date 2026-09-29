from database.database import get_connection


def add_to_cart(product_id, quantity):
    connection = get_connection()

    product = connection.execute(
        """
        SELECT * FROM products
        WHERE id = ?
        """,
        (product_id,)
    ).fetchone()

    if product is None:
        connection.close()
        return None

    existing_item = connection.execute(
        """
        SELECT * FROM cart_items
        WHERE product_id = ?
        """,
        (product_id,)
    ).fetchone()

    if existing_item:
        new_quantity = existing_item["quantity"] + quantity

        connection.execute(
            """
            UPDATE cart_items
            SET quantity = ?
            WHERE id = ?
            """,
            (new_quantity, existing_item["id"])
        )
    else:
        connection.execute(
            """
            INSERT INTO cart_items (product_id, quantity)
            VALUES (?, ?)
            """,
            (product_id, quantity)
        )

    connection.commit()
    connection.close()

    return get_cart()


def get_cart():
    connection = get_connection()

    items = connection.execute(
        """
        SELECT
            cart_items.id,
            cart_items.product_id,
            products.name,
            products.price,
            cart_items.quantity,
            products.price * cart_items.quantity AS subtotal
        FROM cart_items
        JOIN products ON products.id = cart_items.product_id
        ORDER BY cart_items.id DESC
        """
    ).fetchall()

    connection.close()

    cart = [dict(item) for item in items]

    total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "total": total
    }


def update_cart_item(item_id, quantity):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE cart_items
        SET quantity = ?
        WHERE id = ?
        """,
        (quantity, item_id)
    )

    connection.commit()
    updated = cursor.rowcount
    connection.close()

    if updated == 0:
        return None

    return get_cart()


def remove_from_cart(item_id):
    connection = get_connection()

    cursor = connection.execute(
        """
        DELETE FROM cart_items
        WHERE id = ?
        """,
        (item_id,)
    )

    connection.commit()
    deleted = cursor.rowcount
    connection.close()

    if deleted == 0:
        return False

    return True


def clear_cart():
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM cart_items
        """
    )

    connection.commit()
    connection.close()