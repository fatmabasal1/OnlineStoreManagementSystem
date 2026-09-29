import json
import sqlite3
from urllib.request import Request, urlopen

DATABASE_NAME = "store.db"
DUMMY_API = "https://dummyjson.com/products?limit=0"


def get_products():
    request = Request(
        DUMMY_API,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["products"]


def prepare_products(products):
    prepared = []

    for product in products:
        prepared.append({
            "name": product["title"],
            "description": product["description"],
            "price": product["price"],
            "stock": product["stock"],
            "category": product["category"],
            "image_url": product["thumbnail"],
            "rating": product["rating"]
        })

    extra_products = prepared[:6]

    for index, product in enumerate(extra_products, start=1):
        prepared.append({
            "name": f"{product['name']} Edition {index}",
            "description": product["description"],
            "price": product["price"],
            "stock": product["stock"],
            "category": product["category"],
            "image_url": product["image_url"],
            "rating": product["rating"]
        })

    return prepared[:200]


def seed_database():
    products = get_products()
    products = prepare_products(products)

    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute("DELETE FROM cart_items")
    connection.execute("DELETE FROM products")

    for product in products:
        connection.execute(
            """
            INSERT INTO products (
                name,
                description,
                price,
                stock,
                category,
                image_url,
                rating
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                product["name"],
                product["description"],
                product["price"],
                product["stock"],
                product["category"],
                product["image_url"],
                product["rating"]
            )
        )

    connection.commit()

    count = connection.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    connection.close()

    print(f"Successfully added {count} products.")


if __name__ == "__main__":
    seed_database()