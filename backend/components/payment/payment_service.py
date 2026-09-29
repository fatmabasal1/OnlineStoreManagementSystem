from database.database import get_connection


def create_payment():
    connection = get_connection()

    cart_items = connection.execute(
        """
        SELECT
            cart_items.product_id,
            cart_items.quantity,
            products.price,
            products.stock
        FROM cart_items
        JOIN products ON products.id = cart_items.product_id
        """
    ).fetchall()

    if not cart_items:
        connection.close()
        return None

    for item in cart_items:
        if item["quantity"] > item["stock"]:
            connection.close()
            return {
                "success": False,
                "message": "Insufficient stock"
            }

    total_amount = sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )

    cursor = connection.execute(
        """
        INSERT INTO payments (total_amount, status)
        VALUES (?, ?)
        """,
        (total_amount, "Completed")
    )

    payment_id = cursor.lastrowid

    for item in cart_items:
        connection.execute(
            """
            UPDATE products
            SET stock = stock - ?
            WHERE id = ?
            """,
            (item["quantity"], item["product_id"])
        )

    connection.execute(
        """
        DELETE FROM cart_items
        """
    )

    connection.commit()

    payment = connection.execute(
        """
        SELECT * FROM payments
        WHERE id = ?
        """,
        (payment_id,)
    ).fetchone()

    connection.close()

    return {
        "success": True,
        "payment": dict(payment)
    }


def get_payments():
    connection = get_connection()

    payments = connection.execute(
        """
        SELECT * FROM payments
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [dict(payment) for payment in payments]


def get_payment(payment_id):
    connection = get_connection()

    payment = connection.execute(
        """
        SELECT * FROM payments
        WHERE id = ?
        """,
        (payment_id,)
    ).fetchone()

    connection.close()

    if payment is None:
        return None

    return dict(payment)