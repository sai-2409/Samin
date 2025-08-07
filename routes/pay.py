# Yandex Pay routes

from flask import Blueprint, request, jsonify, render_template, session
import uuid, requests, json
from datetime import datetime
from config import YANDEX_MERCHANT_ID, YANDEX_API_URL
from services.email_service import email_service

pay_bp = Blueprint("pay", __name__)

@pay_bp.route("/api/create-yandex-pay-order", methods=["POST"])
def create_yandex_order():
    try:
        data = request.get_json()
        print("Received data:", data)

        cart_items = data.get("cart", [])
        cart_total = data.get("total", "0.00")
        subtotal = data.get("subtotal", "0.00")
        delivery = data.get("delivery", "0.00")
        
        # New fields for enhanced order information
        delivery_date = data.get("deliveryDate", "Не выбрана")
        delivery_notes = data.get("deliveryNotes", [])
        customer_info = data.get("customerInfo", {})
        selected_address_id = data.get("selectedAddressId")

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
                        "onError": f"{request.host_url.rstrip('/')}/cart",
        "onSuccess": f"{request.host_url.rstrip('/')}/payment-success"
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
            
            # Save order to JSON file for tracking with enhanced information
            try:
                # Get user info from session
                user = session.get("user", {})
                user_id = user.get("login") if user else None
                
                # Convert all numeric values to float for consistency
                order_record = {
                    "order_id": order_id,
                    "timestamp": datetime.now().isoformat(),
                    "cart_items": cart_items,
                    "subtotal": float(subtotal),
                    "delivery": float(delivery),
                    "total": float(cart_total),
                    "delivery_date": delivery_date,
                    "delivery_notes": delivery_notes,
                    "customer_info": customer_info,
                    "selected_address_id": selected_address_id,
                    "user_id": user_id,  # Add user ID for review system
                    "yandex_response": response_data,
                    "status": "Оформлен"
                }
                
                # Load existing orders
                try:
                    with open(os.path.join(DATA_DIR, 'orders.json'), 'r', encoding='utf-8') as f:
                        orders = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    orders = []
                
                # Add new order
                orders.append(order_record)
                
                # Save back to file
                with open(os.path.join(DATA_DIR, 'orders.json'), 'w', encoding='utf-8') as f:
                    json.dump(orders, f, ensure_ascii=False, indent=2)
                    
                print(f"Order {order_id} saved to orders.json with enhanced information")
                
                # Store order ID in session for payment success page
                session['last_order_id'] = order_id
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

@pay_bp.route("/payment-success")
def payment_success():
    now = datetime.now()
    
    # Try to get order ID from session or use timestamp
    order_id = session.get('last_order_id', f"{int(now.timestamp() * 1000)}")
    
    # Send email notification for the order
    try:
        # Load the order data from orders.json
        with open(os.path.join(DATA_DIR, 'orders.json'), 'r', encoding='utf-8') as f:
            orders = json.load(f)
        
        # Find the order by ID
        order_data = None
        for order in orders:
            if order.get('order_id') == order_id:
                order_data = order
                break
        
        if order_data:
            # Send email notification
            email_sent = email_service.send_order_notification(order_data)
            if email_sent:
                print(f"Email notification sent for order {order_id}")
            else:
                print(f"Failed to send email notification for order {order_id}")
        else:
            print(f"Order {order_id} not found in orders.json")
            
    except Exception as e:
        print(f"Error sending email notification: {e}")
    
    return render_template('payment_success.html', now=now, order_id=order_id)

@pay_bp.route("/test-email")
def test_email():
    """Test route to verify email functionality"""
    try:
        # Create test order data
        test_order = {
            'order_id': 'test-12345678',
            'customer_info': {
                'name': 'Тестовый Клиент',
                'phone': '+7 (999) 123-45-67',
                'address': 'г. Москва, ул. Тестовая, д. 1'
            },
            'cart_items': [
                {
                    'productName': 'Жареный кешью',
                    'quantity': 2,
                    'price': 949
                },
                {
                    'productName': 'Орехи Макадамия',
                    'quantity': 1,
                    'price': 799
                }
            ],
            'subtotal': 2697,
            'delivery': 0,
            'total': 2697
        }
        
        # Send test email
        email_sent = email_service.send_order_notification(test_order)
        
        if email_sent:
            return jsonify({"success": True, "message": "Test email sent successfully"})
        else:
            return jsonify({"success": False, "message": "Failed to send test email"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
