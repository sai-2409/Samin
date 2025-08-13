# Main routes for the project

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from config import adminPassword, DATA_DIR, PRIVATE_DIR
import json
import os
from datetime import datetime, timedelta
from services.email_service import EmailService
main_bp = Blueprint("main", __name__)


def is_admin_logged_in():
    """Helper function to check if admin is logged in"""
    return bool(session.get("admin_logged_in") or session.get("logged_in"))

def is_user_logged_in():
    """Helper function to check if user is logged in"""
    return bool(session.get("user"))

@main_bp.route('/session-status')
def session_status():
    """Debug route to check current session status"""
    if not is_admin_logged_in():
        return "Access Denied", 403
    
    return {
        "admin_logged_in": session.get("admin_logged_in"),
        "logged_in": session.get("logged_in"),
        "user": session.get("user"),
        "just_logged_in": session.get("just_logged_in"),
        "session_id": session.sid if hasattr(session, 'sid') else None
    }

@main_bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        
        if password == adminPassword:  # Use environment variable
            session["admin_logged_in"] = True  # More specific admin session variable
            session["logged_in"] = True  # Keep for backward compatibility
            return redirect("/admin")
        return "Access Denied", 403
    return render_template("admin_login.html")

@main_bp.route("/logout")
def logout():
    """User logout - only clears user session, preserves admin session"""
    # Only clear user-related session variables
    session.pop("user", None)
    session.pop("just_logged_in", None)
    # Do NOT clear admin session
    return redirect("/")

@main_bp.route("/admin-logout")
def admin_logout():
    """Admin logout - only clears admin session, preserves user session"""
    # Only clear admin-related session variables
    session.pop("admin_logged_in", None)
    session.pop("logged_in", None)
    # Do NOT clear user session
    return redirect("/admin-login")

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
    user = session.get("user")
    just_logged_in = session.pop("just_logged_in", None)
    return render_template("cartSamin.html", user=user, just_logged_in=just_logged_in)

@main_bp.route("/welcome")
def welcome():
    return render_template("welcome__page.html")

@main_bp.route('/admin')
def admin():
    if not is_admin_logged_in():
        return redirect("/admin-login")
        
    try:
        with open(os.path.join(DATA_DIR, 'orders.json'), 'r') as f:
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
        
        # Separate active and delivered orders
        active_orders = []
        delivered_orders = []
        
        for order in orders:
            if order.get('status') == 'Доставлен':
                delivered_orders.append(order)
            else:
                active_orders.append(order)
        
        # Sort active orders by day (newest first) with better timestamp handling
        def get_sort_key(order):
            timestamp = order.get('timestamp', '')
            if not timestamp:
                return '1970-01-01T00:00:00'  # Default for orders without timestamp
            return timestamp
        
        active_orders.sort(key=get_sort_key, reverse=True)
        delivered_orders.sort(key=get_sort_key, reverse=True)
                    
    except (FileNotFoundError, json.JSONDecodeError):
        active_orders = []
        delivered_orders = []

    return render_template('admin.html', active_orders=active_orders, delivered_orders=delivered_orders)

@main_bp.route('/order-tracking')
def order_tracking():
    # Get order ID from query parameter or use a default
    order_id = request.args.get('order_id', '12345')
    
    # Get order details from orders.json
    try:
        with open(os.path.join(DATA_DIR, 'orders.json'), 'r') as f:
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
    # Allow both admin and regular user access
    if not (session.get("logged_in") or session.get("admin_logged_in")):
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
        with open(os.path.join(DATA_DIR, 'orders.json'), 'r') as f:
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
        with open(os.path.join(DATA_DIR, 'orders.json'), 'w') as f:
            json.dump(orders, f, indent=2, ensure_ascii=False)
        
        # Create notification for the user about status change
        user_id = None
        customer_name = "Клиент"
        
        # Find the order to get user info
        for order in orders:
            if order.get('order_id') == order_id:
                user_id = order.get('user_id')
                customer_name = order.get('customer_info', {}).get('name', 'Клиент')
                break
        
        if user_id:
            # Create status-specific notification messages
            status_messages = {
                'Оформлен': 'Ваш заказ был оформлен и принят в обработку.',
                'Собран': 'Ваш заказ собран и готов к отправке.',
                'Отправлен': 'Ваш заказ отправлен и находится в пути.',
                'Доставлен': 'Ваш заказ успешно доставлен! Спасибо за покупку.'
            }
            
            notification = {
                'id': f"status_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'user_id': user_id,
                'type': 'order_status_update',
                'title': f'Статус заказа обновлен: {new_status}',
                'message': f'Заказ #{order_id[:8]} - {status_messages.get(new_status, "Статус заказа был изменен.")}',
                'timestamp': datetime.now().isoformat(),
                'read': False
            }
            
            # Load existing notifications or create new file
            try:
                with open('static/data/notifications.json', 'r') as f:
                    notifications = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                notifications = []
            
            # Add new notification
            notifications.append(notification)
            
            # Save notifications
            with open('static/data/notifications.json', 'w') as f:
                json.dump(notifications, f, indent=2, ensure_ascii=False)
        
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
        with open(os.path.join(DATA_DIR, 'orders.json'), 'r') as f:
            orders = json.load(f)
        
        # Filter orders for current user
        user_orders = [order for order in orders if order.get("user_id") == user["login"]]
        
    except (FileNotFoundError, json.JSONDecodeError):
        user_orders = []
    
    return render_template('user_orders.html', orders=user_orders, user=user)

@main_bp.route('/api/delete-order', methods=['POST'])
def delete_order():
    """Securely delete an order with password verification and user notification"""
    if not session.get("logged_in"):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        admin_password = data.get('admin_password')
        delete_reason = data.get('delete_reason', 'Причина не указана')
        
        if not order_id or not admin_password:
            return jsonify({"success": False, "error": "Missing order_id or password"}), 400
        
        # Verify admin password
        from config import adminPassword
        if admin_password != adminPassword:
            return jsonify({"success": False, "error": "Incorrect password"}), 401
        
        # Load orders from file
        with open(os.path.join(DATA_DIR, 'orders.json'), 'r') as f:
            orders = json.load(f)
        
        # Find the order to delete and get user info for notification
        order_to_delete = None
        for order in orders:
            if order.get('order_id') == order_id:
                order_to_delete = order
                break
        
        if not order_to_delete:
            return jsonify({"success": False, "error": "Order not found"}), 404
        
        # Get user info for notification
        user_id = order_to_delete.get('user_id')
        customer_name = order_to_delete.get('customer_info', {}).get('name', 'Клиент')
        
        # Remove the order
        orders = [order for order in orders if order.get('order_id') != order_id]
        
        # Save updated orders back to file
        with open(os.path.join(DATA_DIR, 'orders.json'), 'w') as f:
            json.dump(orders, f, indent=2, ensure_ascii=False)
        
        # Only create notification if user_id exists
        if user_id:
            notification = {
                'id': f"del_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'user_id': user_id,
                'type': 'order_deleted',
                'title': 'Заказ отменен',
                'message': f'Ваш заказ #{order_id[:8]} был отменен администратором.\n\nПричина: {delete_reason}\n\nЕсли у вас есть вопросы, свяжитесь с нами.',
                'timestamp': datetime.now().isoformat(),
                'read': False
            }
            
            # Load existing notifications or create new file
            try:
                with open('static/data/notifications.json', 'r') as f:
                    notifications = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                notifications = []
            
            # Add new notification
            notifications.append(notification)
            
            # Save notifications
            with open('static/data/notifications.json', 'w') as f:
                json.dump(notifications, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            "success": True, 
            "message": f"Order {order_id[:8]} deleted successfully",
            "customer_name": customer_name
        })
        
    except Exception as e:
        print(f"Error deleting order: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@main_bp.route('/api/get-notifications')
def get_notifications():
    """Get notifications for the current user"""
    user = session.get("user")
    if not user:
        return jsonify({"notifications": []})
    
    try:
        with open(os.path.join(DATA_DIR, 'notifications.json'), 'r') as f:
            notifications = json.load(f)
        
        # Filter notifications for current user (show all, not just unread)
        user_notifications = [
            notif for notif in notifications 
            if notif.get('user_id') == user.get('login')
        ]
        
        # Sort by timestamp (newest first)
        user_notifications.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify({"notifications": user_notifications})
        
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"notifications": []})

@main_bp.route('/api/mark-notification-read', methods=['POST'])
def mark_notification_read():
    """Mark a notification as read"""
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        notification_id = data.get('notification_id')
        
        if not notification_id:
            return jsonify({"success": False, "error": "Missing notification_id"}), 400
        
        # Load notifications
        with open(os.path.join(DATA_DIR, 'notifications.json'), 'r') as f:
            notifications = json.load(f)
        
        # Mark notification as read
        for notif in notifications:
            if notif.get('id') == notification_id and notif.get('user_id') == user.get('login'):
                notif['read'] = True
                break
        
        # Save updated notifications
        with open(os.path.join(DATA_DIR, 'notifications.json'), 'w') as f:
            json.dump(notifications, f, indent=2, ensure_ascii=False)
        
        return jsonify({"success": True})
        
    except Exception as e:
        print(f"Error marking notification as read: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@main_bp.route('/api/daily-orders-data')
def get_daily_orders_data():
    """Get daily orders data for the chart"""
    try:
        from datetime import datetime, timedelta
        import json
        
        # Load orders
        with open(os.path.join(DATA_DIR, 'orders.json'), 'r') as f:
            orders = json.load(f)
        
        # Get last 7 days
        today = datetime.now().date()
        dates = []
        order_counts = []
        
        for i in range(7):
            date = today - timedelta(days=i)
            dates.append(date.strftime('%d.%m'))
            
            # Count orders for this date
            count = 0
            for order in orders:
                if order.get('timestamp'):
                    order_date = datetime.fromisoformat(order['timestamp'].replace('Z', '+00:00')).date()
                    if order_date == date:
                        count += 1
            
            order_counts.append(count)
        
        # Reverse to show oldest to newest
        dates.reverse()
        order_counts.reverse()
        
        # Calculate stats
        today_count = order_counts[-1] if order_counts else 0
        week_total = sum(order_counts)
        week_avg = round(week_total / 7, 1) if week_total > 0 else 0
        
        return jsonify({
            "labels": dates,
            "data": order_counts,
            "stats": {
                "today": today_count,
                "week": week_total,
                "average": week_avg
            }
        })
        
    except Exception as e:
        print(f"Error getting daily orders data: {e}")
        return jsonify({"error": "Failed to load chart data"}), 500

@main_bp.route('/api/check-login')
def check_login():
    """Check if user is logged in"""
    user = session.get("user")
    return jsonify({
        "logged_in": user is not None,
        "user": user
    })

@main_bp.route('/admin/email-notifications')
def admin_email_notifications():
    """Secure route to view email notifications (admin only)"""
    if not session.get("logged_in"):
        return redirect(url_for('main.admin_login'))
    
    try:
        # Get list of email notification files
        import os
        import glob
        from datetime import datetime
        
        email_files = []
        pattern = os.path.join(PRIVATE_DIR, 'email_notifications', 'email_notification_*.html')
        
        for filepath in glob.glob(pattern):
            filename = os.path.basename(filepath)
            order_id = filename.replace('email_notification_', '').replace('.html', '')
            
            # Get file stats
            stat = os.stat(filepath)
            created_time = datetime.fromtimestamp(stat.st_mtime)
            
            email_files.append({
                'filename': filename,
                'order_id': order_id,
                'created_time': created_time.strftime('%d.%m.%Y %H:%M'),
                'filepath': filepath
            })
        
        # Sort by creation time (newest first)
        email_files.sort(key=lambda x: x['created_time'], reverse=True)
        
        return render_template('admin_email_notifications.html', email_files=email_files)
        
    except Exception as e:
        print(f"Error loading email notifications: {e}")
        return "Error loading email notifications", 500

@main_bp.route('/admin/view-email/<order_id>')
def view_email_notification(order_id):
    """View specific email notification (admin only)"""
    if not session.get("logged_in"):
        return redirect(url_for('main.admin_login'))
    
    try:
        import os
        filepath = os.path.join(PRIVATE_DIR, 'email_notifications', f'email_notification_{order_id}.html')
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        else:
            return "Email notification not found", 404
            
    except Exception as e:
        print(f"Error viewing email notification: {e}")
        return "Error viewing email notification", 500