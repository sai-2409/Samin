import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os

class EmailService:
    def __init__(self):
        # Email service configuration
        from config import EMAIL_USER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
        
        # Use configuration variables instead of hardcoded values
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        
        self.sender_email = EMAIL_USER
        self.sender_password = EMAIL_PASSWORD
        
    def send_order_notification(self, order_data, admin_email=None):
        if admin_email is None:
            from config import ADMIN_EMAIL
            admin_email = ADMIN_EMAIL
        """
        Send email notification when a new order is placed and paid
        """
        try:
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = admin_email
            msg['Subject'] = f"Новый заказ #{order_data['order_id'][:8]}"
            
            # Create HTML content
            html_content = self._create_order_email_html(order_data)
            
            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))
            
            # Send email
            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
                    
                print(f"Order notification email sent successfully to {admin_email}")
                return True
                
            except Exception as smtp_error:
                print(f"SMTP Error: {smtp_error}")
                print("Saving email content to file as backup...")
                
                # Save email content to file as backup
                html_content = self._create_order_email_html(order_data)
                from config import PRIVATE_DIR
                filename = os.path.join(PRIVATE_DIR, 'email_notifications', f'email_notification_{order_data["order_id"][:8]}.html')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"Email content saved to {filename}")
                return True
            
        except Exception as e:
            print(f"Error sending email notification: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_order_email_html(self, order_data):
        """
        Create HTML email content for order notification
        """
        order_id = order_data['order_id'][:8]
        customer_name = order_data.get('customer_info', {}).get('name', 'Клиент')
        customer_phone = order_data.get('customer_info', {}).get('phone', 'Не указан')
        customer_address = order_data.get('customer_info', {}).get('address', 'Не указан')
        total_amount = order_data.get('total', 0)
        delivery_cost = order_data.get('delivery', 0)
        subtotal = order_data.get('subtotal', 0)
        
        # Format items for email
        items_html = ""
        for item in order_data.get('cart_items', []):
            item_name = item.get('productName', 'Товар')
            item_quantity = item.get('quantity', 1)
            item_price = item.get('price', 0)
            item_total = item_quantity * item_price
            
            items_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{item_name}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">{item_quantity}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: right;">{item_price} ₽</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: right;">{item_total} ₽</td>
            </tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Новый заказ #{order_id}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #8B3000, #FFC338);
                    color: white;
                    padding: 20px;
                    border-radius: 10px 10px 0 0;
                    text-align: center;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 20px;
                    border-radius: 0 0 10px 10px;
                }}
                .order-info {{
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 15px 0;
                    border-left: 4px solid #8B3000;
                }}
                .customer-info {{
                    background: #e8f5e8;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 15px 0;
                }}
                .items-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                }}
                .items-table th {{
                    background: #8B3000;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }}
                .items-table td {{
                    padding: 10px;
                    border-bottom: 1px solid #eee;
                }}
                .total-section {{
                    background: #f0f8ff;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 15px 0;
                }}
                .total-row {{
                    display: flex;
                    justify-content: space-between;
                    margin: 5px 0;
                }}
                .total-final {{
                    font-weight: bold;
                    font-size: 1.2em;
                    color: #8B3000;
                    border-top: 2px solid #8B3000;
                    padding-top: 10px;
                    margin-top: 10px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    padding: 15px;
                    background: #f5f5f5;
                    border-radius: 8px;
                }}
                .status-badge {{
                    background: #4CAF50;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    display: inline-block;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎉 Новый заказ #{order_id}</h1>
                <p>Получен новый оплаченный заказ в магазине Samin</p>
                <div class="status-badge">Оплачен ✓</div>
            </div>
            
            <div class="content">
                <div class="order-info">
                    <h3>📋 Информация о заказе</h3>
                    <p><strong>Номер заказа:</strong> #{order_id}</p>
                    <p><strong>Дата и время:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
                    <p><strong>Статус:</strong> <span class="status-badge">Оплачен</span></p>
                </div>
                
                <div class="customer-info">
                    <h3>👤 Информация о клиенте</h3>
                    <p><strong>Имя:</strong> {customer_name}</p>
                    <p><strong>Телефон:</strong> {customer_phone}</p>
                    <p><strong>Адрес доставки:</strong> {customer_address}</p>
                </div>
                
                <h3>🛒 Товары в заказе</h3>
                <table class="items-table">
                    <thead>
                        <tr>
                            <th>Товар</th>
                            <th style="text-align: center;">Кол-во</th>
                            <th style="text-align: right;">Цена</th>
                            <th style="text-align: right;">Сумма</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_html}
                    </tbody>
                </table>
                
                <div class="total-section">
                    <h3>💰 Итоговая сумма</h3>
                    <div class="total-row">
                        <span>Сумма товаров:</span>
                        <span>{subtotal} ₽</span>
                    </div>
                    <div class="total-row">
                        <span>Доставка:</span>
                        <span>{delivery_cost} ₽</span>
                    </div>
                    <div class="total-row total-final">
                        <span>Итого к оплате:</span>
                        <span>{total_amount} ₽</span>
                    </div>
                </div>
                
                <div class="footer">
                    <p>📧 Это автоматическое уведомление о новом заказе</p>
                    <p>🕒 Время получения: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
                    <p>💼 Магазин Samin - Ваши любимые орехи и сухофрукты</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

# Create global instance
email_service = EmailService() 