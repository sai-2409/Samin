# Samin - E-commerce Platform

A modern e-commerce platform built with Flask, featuring Yandex Pay integration, user authentication, and order management.

## Features

- 🛒 Shopping cart functionality
- 💳 Yandex Pay integration
- 👤 User authentication via Yandex OAuth
- 📦 Order tracking system
- ⭐ Review system
- 🗺️ Address suggestions with DaData API
- 📍 Yandex Maps integration
- 👨‍💼 Admin dashboard

## Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd samin
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**

   - Copy `env.example` to `.env`
   - Fill in your API keys and configuration:
     ```bash
     cp env.example .env
     ```

5. **Required Environment Variables**

   ```env
   # Yandex OAuth
   CLIENT_ID=your_yandex_client_id
   CLIENT_SECRET=your_yandex_client_secret
   REDIRECT_URI=http://localhost:5000/auth/callback

   # Yandex Pay
   YANDEX_MERCHANT_ID=your_merchant_id
   YANDEX_API_URL=https://pay.yandex.ru/api/v1/orders

   # Flask
   SECRET_KEY=your_secret_key

   # Admin
   adminPassword=your_admin_password

   # API Keys
   DADATA_API_TOKEN=your_dadata_token
   YANDEX_MAPS_API_KEY=your_yandex_maps_key
   ```

6. **Run the application**

   ```bash
   python app.py
   ```

7. **Access the application**
   - Main site: http://localhost:5000
   - Admin dashboard: http://localhost:5000/admin

## Security Notes

- All sensitive data is stored in environment variables
- API keys are loaded from `.env` file (not committed to git)
- Admin password is configurable via environment variable

## API Keys Required

- **Yandex OAuth**: For user authentication
- **Yandex Pay**: For payment processing
- **DaData**: For address suggestions
- **Yandex Maps**: For map functionality

## License

[Your License Here]
