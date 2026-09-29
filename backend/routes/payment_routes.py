from flask import Blueprint, jsonify

from components.payment.payment_service import (
    create_payment,
    get_payments,
    get_payment
)


payment_bp = Blueprint(
    "payment",
    __name__,
    url_prefix="/api/payments"
)


@payment_bp.route("", methods=["POST"])
def create():
    result = create_payment()

    if result is None:
        return jsonify({
            "message": "Cart is empty"
        }), 400

    if not result["success"]:
        return jsonify({
            "message": result["message"]
        }), 400

    return jsonify(result["payment"]), 201


@payment_bp.route("", methods=["GET"])
def get_all():
    payments = get_payments()
    return jsonify(payments), 200


@payment_bp.route("/<int:payment_id>", methods=["GET"])
def get_one(payment_id):
    payment = get_payment(payment_id)

    if payment is None:
        return jsonify({
            "message": "Payment not found"
        }), 404

    return jsonify(payment), 200