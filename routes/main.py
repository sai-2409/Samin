# Main routes for the project

from flask import Blueprint, render_template, session, request, redirect, jsonify, url_for
import json
from datetime import datetime, timedelta
from config import adminPassword

main_bp = Blueprint("main", __name__)

@main_bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        
        if password == adminPassword:  # Use environment variable
            session["logged_in"] = True
            return redirect("/admin")
        return "Access Denied", 403
    return render_template("admin_login.html")

@main_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect("/")

@main_bp.route("/")
def index():
    user = session.get("user")
    just_logged_in = session.pop("just_logged_in", None)
    return render_template("index.html", user=user, just_logged_in=just_logged_in)

@main_bp.route("/calculator")
def calculator():
    return render_template("calc.html")

@main_bp.route("/cart")
def cart():
    return render_template("cartSamin.html")

@main_bp.route("/welcome")
def welcome():
    return render_template("welcome__page.html")

@main_bp.route('/admin')
def admin():
    if not session.get("logged_in"):
        return redirect("/admin-login")
        
    try:
        with open('static/data/orders.json', 'r') as f:
            orders = json.load(f)
            
        # Convert any string totals to float for consistency
        for order in orders:
            if isinstance(order.get('total'), str):
                try:
                    order['total'] = float(order['total'])
                except (ValueError, TypeError):
                    order['total'] = 0.0
            if isinstance(order.get('subtotal'), str):
                try:
                    order['subtotal'] = float(order['subtotal'])
                except (ValueError, TypeError):
                    order['subtotal'] = 0.0
            if isinstance(order.get('delivery'), str):
                try:
                    order['delivery'] = float(order['delivery'])
                except (ValueError, TypeError):
                    order['delivery'] = 0.0
                    
    except (FileNotFoundError, json.JSONDecodeError):
        orders = []

    return render_template('admin.html', orders=orders)

@main_bp.route('/order-tracking')
def order_tracking():
    # Get order ID from query parameter or use a default
    order_id = request.args.get('order_id', '12345')
    
    # Get order details from orders.json
    try:
        with open('static/data/orders.json', 'r') as f:
            orders = json.load(f)
        
        # Find the specific order
        order = None
        for o in orders:
            if o.get('order_id') == order_id:
                order = o
                break
        
        if not order:
            # Use default values if order not found
            order = {
                'order_id': order_id,
                'timestamp': datetime.now().isoformat(),
                'total': 1500.00,
                'delivery_method': 'Курьерская доставка',
                'delivery_address': 'г. Москва, ул. Примерная, д. 1, кв. 1',
                'expected_date': '15 августа 2024'
            }
    except (FileNotFoundError, json.JSONDecodeError):
        # Use default values if file not found
        order = {
            'order_id': order_id,
            'timestamp': datetime.now().isoformat(),
            'total': 1500.00,
            'delivery_method': 'Курьерская доставка',
            'delivery_address': 'г. Москва, ул. Примерная, д. 1, кв. 1',
            'expected_date': '15 августа 2024'
        }
    
    # Format dates
    order_date = datetime.fromisoformat(order['timestamp']).strftime('%d.%m.%Y')
    order_placed_time = datetime.fromisoformat(order['timestamp']).strftime('%H:%M')
    payment_time = datetime.fromisoformat(order['timestamp']).strftime('%H:%M')
    
    # Extract real order data
    cart_items = order.get('cart_items', [])
    customer_info = order.get('customer_info', {})
    delivery_notes = order.get('delivery_notes', [])
    delivery_date = order.get('delivery_date', '15 августа 2024')
    
    # Get delivery address from customer info or fallback
    delivery_address = customer_info.get('address', order.get('delivery_address', 'г. Москва, ул. Примерная, д. 1, кв. 1'))
    
    # Calculate expected date from delivery_date field
    if delivery_date and 'Завтра' in delivery_date:
        tomorrow = datetime.now() + timedelta(days=1)
        expected_date = tomorrow.strftime('%d.%m.%Y')
    elif delivery_date and 'сб' in delivery_date:
        # Extract date from delivery_date string like "сб, 09.08"
        try:
            date_part = delivery_date.split(',')[1].strip().split('₽')[0].strip()
            # Clean up the date format - extract only day and month
            if '.' in date_part:
                parts = date_part.split('.')
                if len(parts) >= 2:
                    day = parts[0]
                    month = parts[1][:2]  # Take only first 2 digits of month
                    expected_date = f"{day}.{month}.2024"
                else:
                    expected_date = '15 августа 2024'
            else:
                expected_date = '15 августа 2024'
        except:
            expected_date = '15 августа 2024'
    else:
        # Default to tomorrow if no specific date found
        tomorrow = datetime.now() + timedelta(days=1)
        expected_date = tomorrow.strftime('%d.%m.%Y')
    
    # Get order status and update time
    order_status = order.get('status', 'Оформлен')
    status_updated_at = None
    if order.get('status_updated_at'):
        try:
            status_time = datetime.fromisoformat(order['status_updated_at'])
            status_updated_at = status_time.strftime('%H:%M')
        except:
            status_updated_at = None
    
    return render_template('order_tracking.html',
                         order_id=order['order_id'],
                         order_date=order_date,
                         order_placed_time=order_placed_time,
                         payment_time=payment_time,
                         order_total=f"{order['total']:.2f}",
                         delivery_method='Курьерская доставка',
                         delivery_address=delivery_address,
                         expected_date=expected_date,
                         cart_items=cart_items,
                         customer_info=customer_info,
                         delivery_notes=delivery_notes,
                         delivery_date=delivery_date,
                         order_status=order_status,
                         status_updated_at=status_updated_at)

@main_bp.route('/api/update-order-status', methods=['POST'])
def update_order_status():
    if not session.get("logged_in"):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        new_status = data.get('status')
        
        if not order_id or not new_status:
            return jsonify({"success": False, "error": "Missing order_id or status"}), 400
        
        # Valid statuses
        valid_statuses = ['Оформлен', 'Собран', 'Отправлен', 'Доставлен']
        if new_status not in valid_statuses:
            return jsonify({"success": False, "error": "Invalid status"}), 400
        
        # Load orders from file
        with open('static/data/orders.json', 'r') as f:
            orders = json.load(f)
        
        # Find and update the order
        order_updated = False
        for order in orders:
            if order.get('order_id') == order_id:
                order['status'] = new_status
                order['status_updated_at'] = datetime.now().isoformat()
                order_updated = True
                break
        
        if not order_updated:
            return jsonify({"success": False, "error": "Order not found"}), 404
        
        # Save updated orders back to file
        with open('static/data/orders.json', 'w') as f:
            json.dump(orders, f, indent=2, ensure_ascii=False)
        
        return jsonify({"success": True, "message": "Order status updated successfully"})
        
    except Exception as e:
        print(f"Error updating order status: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@main_bp.route('/api/get-api-keys')
def get_api_keys():
    """Safely provide API keys to frontend"""
    from config import DADATA_API_TOKEN, YANDEX_MAPS_API_KEY, YANDEX_MERCHANT_ID
    return jsonify({
        'dadata_token': DADATA_API_TOKEN,
        'yandex_maps_key': YANDEX_MAPS_API_KEY,
        'yandex_merchant_id': YANDEX_MERCHANT_ID
    })

@main_bp.context_processor
def inject_config():
    """Make config variables available in templates"""
    from config import YANDEX_MAPS_API_KEY
    return dict(config={'YANDEX_MAPS_API_KEY': YANDEX_MAPS_API_KEY})

@main_bp.route('/user_orders')
def user_orders():
    """User orders page - requires login"""
    user = session.get("user")
    if not user:
        return redirect("/login")
    
    try:
        with open('static/data/orders.json', 'r') as f:
            orders = json.load(f)
        
        # Filter orders for current user
        user_orders = [order for order in orders if order.get("user_id") == user["login"]]
        
    except (FileNotFoundError, json.JSONDecodeError):
        user_orders = []
    
    return render_template('user_orders.html', orders=user_orders, user=user)
