# Render Configuration Template
# This file shows the required environment variables for deploying on Render
# Copy these to your Render dashboard: Service → Environment → Environment Variables

"""
REQUIRED ENVIRONMENT VARIABLES FOR RENDER:

# OAuth Configuration
CLIENT_ID=your_yandex_oauth_client_id
CLIENT_SECRET=your_yandex_oauth_client_secret
REDIRECT_URI=https://your-app-name.onrender.com/callback

# Yandex Payment Configuration
YANDEX_MERCHANT_ID=your_yandex_merchant_id
YANDEX_API_URL=https://yoomoney.ru/api/v4

# Security
SECRET_KEY=your_secret_key_here


# API Keys
DADATA_API_TOKEN=your_dadata_api_token
YANDEX_MAPS_API_KEY=your_yandex_maps_api_key

# Email Configuration
EMAIL_USER=your_email@yandex.ru
EMAIL_PASSWORD=your_app_password
ADMIN_EMAIL=admin@samin.ru

# Server Configuration
DEBUG_MODE=False
HOST=0.0.0.0
PORT=10000

# Optional - File Paths (Render will use these automatically)
DATA_DIR=/opt/render/project/src/static/data
PRIVATE_DIR=/opt/render/project/src/private
UPLOADS_DIR=/opt/render/project/src/static/uploads

# Optional - Email Service
SMTP_SERVER=smtp.yandex.ru
SMTP_PORT=587

# Optional - File Upload
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,webp

# Optional - Application Info
APP_NAME=Samin
APP_VERSION=1.0.0

RENDER-SPECIFIC VARIABLES (Set automatically by Render):
RENDER=true
RENDER_EXTERNAL_HOSTNAME=your-app-name.onrender.com
RENDER_SERVICE_ID=your_service_id
RENDER_SERVICE_NAME=your_service_name
RENDER_INSTANCE_ID=your_instance_id
"""

# This file is for reference only - delete it after setting up your environment variables 