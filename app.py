# This code will run html files on the mini server with Flask
import os
import requests
import json
import uuid
from datetime import datetime
from flask import (
    Flask,
    redirect,
    request,
    session,
    url_for,
    render_template,
    jsonify
)


app = Flask(__name__)
app.secret_key = 'your_secret_key'

CLIENT_ID = "cb0aaca9b73140c4b8fd5d279875b8c0"
CLIENT_SECRET = "f9d87c4baa2f45f985cf6936b32cb9ea"
REDIRECT_URI = "https://xxxx.ngrok-free.app/callback"  # Replace with your ngrok URL like: "https://abc123.ngrok.io/callback"

# === Yandex Pay Настройки ===
YANDEX_MERCHANT_ID = "54281716-0b74-4b0e-bf61-bc6c45b67f5c"
YANDEX_API_URL = "https://sandbox.pay.yandex.ru/api/merchant/v1/orders"
 # Get this from your Yandex Pay dashboard

@app.route("/")
def index():
    user = session.get("user")
    just_logged_in = session.pop("just_logged_in", None)
    return render_template("index.html", user=user, just_logged_in=just_logged_in)

@app.route("/calculator")
def calculator():
    return render_template('calc.html')

@app.route("/cart")
def cart():
    return render_template('cartSamin.html')

@app.route("/welcome")
def welcome():
    return render_template('welcome__page.html')

@app.route("/login")
def login():
    return redirect(
        f"https://oauth.yandex.com/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    )

# Admin dashboard 
# @app.route('/admin')
# def admin():
#     try:
#         with open('static/data/orders.json', 'r') as f:
#             orders = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         orders = []

#     return render_template('admin.html', orders=orders)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Ошибка авторизации"
    token_res = requests.post("https://oauth.yandex.com/token", data={
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    token_json = token_res.json()
    access_token = token_json.get("access_token")
    if not access_token:
        return "Ошибка получения токена"
    user_info = requests.get("https://login.yandex.ru/info", headers={
        "Authorization": f"OAuth {access_token}"
    }).json()
    session["user"] = {
        "login": user_info["login"],
        "avatar": user_info.get("default_avatar_id")
    }
    session["just_logged_in"] = True
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/api/create-yandex-pay-order", methods=["POST"])
def create_yandex_order():
    try:
        data = request.get_json()
        print("Received data:", data)

        cart_items = data.get("cart", [])
        cart_total = data.get("total", "0.00")
        subtotal = data.get("subtotal", "0.00")
        delivery = data.get("delivery", "0.00")

        # Validate cart data
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400

        order_id = str(uuid.uuid4())
        print(f"Generated order ID: {order_id}")

        # Преобразуем товары в формат Яндекс Пэй
        items = []
        for item in cart_items:
            try:
                price = float(item.get("price", 0))
                quantity = int(item.get("quantity", 1))
                item_total = price * quantity
                
                items.append({
                    "discountedUnitPrice": str(price),
                    "productId": str(item.get("id", f"item-{len(items)}")),
                    "title": item.get("name", "Товар"),
                    "total": str(item_total),
                    "quantity": { "count": str(quantity) }
                })
                print(f"Added item: {item.get('name')} - {quantity}x {price} = {item_total}")
            except (ValueError, TypeError) as e:
                print(f"Error processing item {item}: {e}")
                continue

        # Add delivery as a separate item if delivery cost > 0
        if float(delivery) > 0:
            items.append({
                "discountedUnitPrice": delivery,
                "productId": "delivery",
                "title": "Доставка",
                "total": delivery,
                "quantity": { "count": "1" }
            })
            print(f"Added delivery: {delivery}")

        # Use the provided total (which includes delivery)
        cart_total = str(float(cart_total))
        print(f"Final total with delivery: {cart_total}")

        payload = {
            "orderId": order_id,
            "availablePaymentMethods": ["CARD", "SPLIT"],
            "purpose": "Оплата заказа в магазине Samin",
            "cart": {
                "items": items,
                "total": {
                    "amount": cart_total
                }
            },
            "currencyCode": "RUB",
            "redirectUrls": {
                "onError": "http://127.0.0.1:5000/cart",
                "onSuccess": "http://127.0.0.1:5000/payment-success"
            },
            "ttl": 86400
        }

        print("Sending payload to Yandex Pay:", payload)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"API-Key {YANDEX_MERCHANT_ID}"
        }

        response = requests.post(YANDEX_API_URL, json=payload, headers=headers)
        print(f"Yandex Pay response status: {response.status_code}")
        print(f"Yandex Pay response: {response.text}")

        if response.status_code == 200:
            response_data = response.json()
            
            # Save order to JSON file for tracking
            try:
                order_record = {
                    "order_id": order_id,
                    "timestamp": datetime.now().isoformat(),
                    "cart_items": cart_items,
                    "subtotal": subtotal,
                    "delivery": delivery,
                    "total": cart_total,
                    "yandex_response": response_data
                }
                
                # Load existing orders
                try:
                    with open('static/data/orders.json', 'r', encoding='utf-8') as f:
                        orders = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    orders = []
                
                # Add new order
                orders.append(order_record)
                
                # Save back to file
                with open('static/data/orders.json', 'w', encoding='utf-8') as f:
                    json.dump(orders, f, ensure_ascii=False, indent=2)
                    
                print(f"Order {order_id} saved to orders.json")
            except Exception as e:
                print(f"Error saving order to file: {e}")
            
            return jsonify(response_data)
        else:
            return jsonify({
                "error": "Yandex Pay API failed", 
                "status_code": response.status_code,
                "details": response.text
            }), 400

    except Exception as e:
        print(f"Error in create_yandex_order: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/payment-success")
def payment_success():
    now = datetime.now()
    return render_template('payment_success.html', now=now)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
