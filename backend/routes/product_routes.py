from flask import Blueprint, request, jsonify

from components.product.product_service import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product
)


product_bp = Blueprint("product", __name__, url_prefix="/api/products")


@product_bp.route("", methods=["POST"])
def create():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body is required"}), 400

    name = data.get("name")
    description = data.get("description", "")
    price = data.get("price")
    stock = data.get("stock", 0)
    category = data.get("category", "")

    if not name:
        return jsonify({"message": "Product name is required"}), 400

    if price is None or price < 0:
        return jsonify({"message": "Price must be a non-negative number"}), 400

    if stock < 0:
        return jsonify({"message": "Stock cannot be negative"}), 400

    product = create_product(
        name,
        description,
        price,
        stock,
        category
    )

    return jsonify(product), 201


@product_bp.route("", methods=["GET"])
def get_all():
    products = get_products()
    return jsonify(products), 200


@product_bp.route("/<int:product_id>", methods=["GET"])
def get_one(product_id):
    product = get_product(product_id)

    if product is None:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product), 200


@product_bp.route("/<int:product_id>", methods=["PUT"])
def update(product_id):
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body is required"}), 400

    name = data.get("name")
    description = data.get("description", "")
    price = data.get("price")
    stock = data.get("stock", 0)
    category = data.get("category", "")

    if not name:
        return jsonify({"message": "Product name is required"}), 400

    if price is None or price < 0:
        return jsonify({"message": "Price must be a non-negative number"}), 400

    if stock < 0:
        return jsonify({"message": "Stock cannot be negative"}), 400

    product = update_product(
        product_id,
        name,
        description,
        price,
        stock,
        category
    )

    if product is None:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product), 200


@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete(product_id):
    deleted = delete_product(product_id)

    if not deleted:
        return jsonify({"message": "Product not found"}), 404

    return jsonify({"message": "Product deleted successfully"}), 200