# This code will run html files on the mini server with Flask
import os
import requests
import json
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

YANDEX_PAY_API_URL = "https://sandbox.pay.yandex.ru/api/merchant/v1/orders"
YANDEX_PAY_MERCHANT_ID = "54281716-0b74-4b0e-bf61-bc6c45b67f5c"
YANDEX_PAY_API_KEY = "54281716-0b74-4b0e-bf61-bc6c45b67f5c"
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
@app.route('/admin')
def admin():
    try:
        with open('static/data/orders.json', 'r') as f:
            orders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = []

    return render_template('admin.html', orders=orders)


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

@app.route('/api/create-yandex-pay-order', methods=['POST'])
def create_yandex_pay_order():
    print("=== PAYMENT API CALLED ===")
    print("Request headers:", dict(request.headers))
    print("Request method:", request.method)
    
    try:
        order_data = request.json
        print("Order data received:", order_data)
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"error": "Invalid JSON data"}), 400
    
    # Get the base URL from the request
    base_url = request.host_url.rstrip('/')
    print("Base URL:", base_url)
    
    if 'ngrok' in base_url:
        # If accessed via ngrok, use ngrok URL
        return_url = "https://xxxx.ngrok-free.app/payment-success"
    else:
        # If accessed via localhost, use localhost URL
        return_url = "http://127.0.0.1:5000/payment-success"
    
    print("Return URL:", return_url)

    amount_value = order_data["amount"]
    quantity = 1
    item_total = float(amount_value) * quantity

    payload = {
    "merchantId": YANDEX_PAY_MERCHANT_ID,
    "orderId": "ORDER12345",
    "amount": {
        "value": 15980.00,
        "currency": "RUB"
    },
    "currencyCode": "RUB",
    "cart": {
        "items": [
            {
                "productId": "sku-1",
                "name": "Product Name",
                "quantity": quantity,
                "price": {
                    "amount": 15980.00,
                    "currency": "RUB"
                },
                "total": item_total
            }
        ],
        "total": item_total
    },
    "description": "Order from Samin Shop",
    "confirmation": {
        "type": "redirect",
        "returnUrl": return_url  # ✅ используем уже рассчитанный выше
    }
}


    # Debug: print types of cart fields
    item = payload["cart"]["items"][0]
    print("DEBUG types:")
    print("quantity:", item["quantity"], type(item["quantity"]))
    print("price:", item["price"], type(item["price"]))
    print("total:", item["total"], type(item["total"]))
    print("cart total:", payload["cart"]["total"], type(payload["cart"]["total"]))

    headers = {
        "Authorization": f"Api-Key {YANDEX_PAY_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(YANDEX_PAY_API_URL, json=payload, headers=headers)

    print("Sent payload:", json.dumps(payload, indent=2))
    print("Yandex Pay response:", response.text)

    if response.status_code == 200:
        payment_url = response.json()["confirmation"]["confirmation_url"]
        return jsonify({"payment_url": payment_url})
    else:
        print("Yandex Pay API error:", response.text)
        return jsonify({"error": response.text}), 400

@app.route("/payment-success")
def payment_success():
    return render_template("payment_success.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# Putting Yandex ID avatar in the header
# session["user"] = {
#     "login": user_info["login"],
#     "avatar": user_info.get("default_avatar_id")
# }

