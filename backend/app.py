from flask import Flask, jsonify
from flask_cors import CORS

from database.database import init_database
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.payment_routes import payment_bp


app = Flask(__name__)
CORS(app)

init_database()

app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(payment_bp)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Online Store Management System API is running"
    })


if __name__ == "__main__":
    app.run(debug=True)