from flask import Blueprint, request, jsonify

from components.cart.cart_service import (
    add_to_cart,
    get_cart,
    update_cart_item,
    remove_from_cart,
    clear_cart
)


cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")


@cart_bp.route("", methods=["GET"])
def get():
    cart = get_cart()
    return jsonify(cart), 200


@cart_bp.route("/items", methods=["POST"])
def add():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body is required"}), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if product_id is None or quantity is None:
        return jsonify({
            "message": "Product ID and quantity are required"
        }), 400

    if quantity <= 0:
        return jsonify({
            "message": "Quantity must be greater than zero"
        }), 400

    cart = add_to_cart(product_id, quantity)

    if cart is None:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(cart), 201


@cart_bp.route("/items/<int:item_id>", methods=["PUT"])
def update(item_id):
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body is required"}), 400

    quantity = data.get("quantity")

    if quantity is None:
        return jsonify({"message": "Quantity is required"}), 400

    if quantity <= 0:
        return jsonify({
            "message": "Quantity must be greater than zero"
        }), 400

    cart = update_cart_item(item_id, quantity)

    if cart is None:
        return jsonify({"message": "Cart item not found"}), 404

    return jsonify(cart), 200


@cart_bp.route("/items/<int:item_id>", methods=["DELETE"])
def remove(item_id):
    removed = remove_from_cart(item_id)

    if not removed:
        return jsonify({"message": "Cart item not found"}), 404

    return jsonify({
        "message": "Item removed from cart"
    }), 200


@cart_bp.route("/clear", methods=["DELETE"])
def clear():
    clear_cart()

    return jsonify({
        "message": "Cart cleared successfully"
    }), 200