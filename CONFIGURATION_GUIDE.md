# Configuration Guide

## 🔧 Environment Variables

This guide documents all the configuration variables that have been moved from hardcoded values to environment variables.

### **Required Environment Variables**

Create a `.env` file in your project root with the following variables:

#### **Yandex OAuth Configuration**

```bash
CLIENT_ID=your_yandex_client_id
CLIENT_SECRET=your_yandex_client_secret
REDIRECT_URI=http://localhost:5000/callback
```

#### **Yandex Pay Configuration**

```bash
YANDEX_MERCHANT_ID=your_yandex_merchant_id
YANDEX_API_URL=https://api.yookassa.ru/v3/payments
```

#### **Security**

```bash
SECRET_KEY=your_secret_key_here
adminPassword=your_admin_password
```

#### **API Keys**

```bash
DADATA_API_TOKEN=your_dadata_api_token
YANDEX_MAPS_API_KEY=your_yandex_maps_api_key
```

#### **Email Configuration**

```bash
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
ADMIN_EMAIL=admin@samin.ru
```

### **Optional Environment Variables (with defaults)**

#### **Server Configuration**

```bash
DEBUG_MODE=True          # Default: True
HOST=0.0.0.0           # Default: 0.0.0.0
PORT=5000               # Default: 5000
```

#### **Email Service Configuration**

```bash
SMTP_SERVER=smtp.gmail.com  # Default: smtp.gmail.com
SMTP_PORT=587               # Default: 587
```

#### **File Paths Configuration**

```bash
DATA_DIR=static/data         # Default: static/data
PRIVATE_DIR=private          # Default: private
UPLOADS_DIR=static/uploads   # Default: static/uploads
```

#### **File Upload Configuration**

```bash
MAX_FILE_SIZE=5242880        # Default: 5MB (5242880 bytes)
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,webp  # Default: png,jpg,jpeg,gif,webp
```

#### **Application Settings**

```bash
APP_NAME=Samin              # Default: Samin
APP_VERSION=1.0.0           # Default: 1.0.0
```

## 🔄 Changes Made

### **Files Updated:**

1. **`config.py`** - Added new configuration variables
2. **`app.py`** - Now uses `DEBUG_MODE`, `HOST`, `PORT` from config
3. **`services/email_service.py`** - Now uses `SMTP_SERVER`, `SMTP_PORT` from config
4. **`routes/main.py`** - Now uses `DATA_DIR`, `PRIVATE_DIR` for file paths
5. **`routes/pay.py`** - Now uses `DATA_DIR` for file paths
6. **`routes/review.py`** - Now uses `DATA_DIR`, `UPLOADS_DIR`, `ALLOWED_EXTENSIONS`, `MAX_FILE_SIZE` from config

### **Hardcoded Values Removed:**

- ✅ Server port (5001 → configurable)
- ✅ Debug mode (True → configurable)
- ✅ SMTP server (smtp.gmail.com → configurable)
- ✅ SMTP port (587 → configurable)
- ✅ File paths (static/data/ → configurable)
- ✅ Upload settings (file size, extensions → configurable)

## 🚀 Benefits

1. **Environment-specific configuration** - Different settings for development, staging, production
2. **Security** - Sensitive data not in code
3. **Flexibility** - Easy to change settings without code changes
4. **Deployment ready** - Works with containerization and cloud platforms
5. **Team collaboration** - Each developer can have their own .env file

## 📝 Example .env File

```bash
# Copy this to .env and fill in your values
CLIENT_ID=your_yandex_client_id
CLIENT_SECRET=your_yandex_client_secret
REDIRECT_URI=http://localhost:5000/callback
YANDEX_MERCHANT_ID=your_yandex_merchant_id
YANDEX_API_URL=https://api.yookassa.ru/v3/payments
SECRET_KEY=your_secret_key_here
adminPassword=your_admin_password
DADATA_API_TOKEN=your_dadata_api_token
YANDEX_MAPS_API_KEY=your_yandex_maps_api_key
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
ADMIN_EMAIL=admin@samin.ru
DEBUG_MODE=True
HOST=0.0.0.0
PORT=5000
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
DATA_DIR=static/data
PRIVATE_DIR=private
UPLOADS_DIR=static/uploads
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,webp
APP_NAME=Samin
APP_VERSION=1.0.0
```
