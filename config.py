# Keys,Ids,Tokens,etc.

from dotenv import load_dotenv
import os
import platform
import socket

# Load environment variables
load_dotenv()  # Загружает переменные из .env

def is_running_on_render():
    """Detect if the application is running on Render"""
    # Check for Render-specific environment variables
    render_env_vars = [
        'RENDER',
        'RENDER_EXTERNAL_HOSTNAME',
        'RENDER_INSTANCE_ID',
        'RENDER_SERVICE_ID',
        'RENDER_SERVICE_NAME'
    ]
    
    # Check if any Render environment variables are set
    if any(os.getenv(var) for var in render_env_vars):
        return True
    
    # Check hostname for Render patterns
    try:
        hostname = socket.gethostname()
        if 'render' in hostname.lower():
            return True
    except:
        pass
    
    # Check for common cloud hosting patterns
    cloud_indicators = [
        'RENDER',
        'HEROKU',
        'VERCEL',
        'NETLIFY',
        'DIGITALOCEAN',
        'AWS',
        'GCP',
        'AZURE'
    ]
    
    for indicator in cloud_indicators:
        if os.getenv(indicator) or os.getenv(f'{indicator}_APP_ID'):
            return True
    
    return False

def get_env_with_fallback(key, default=None, required=False):
    """Get environment variable with fallback and validation"""
    value = os.getenv(key, default)
    
    if required and not value:
        if is_running_on_render():
            raise ValueError(f"Required environment variable {key} not set on Render. Please configure it in your Render dashboard.")
        else:
            raise ValueError(f"Required environment variable {key} not set. Please check your .env file or environment configuration.")
    
    return value

def log_environment_info():
    """Log environment information for debugging"""
    is_render = is_running_on_render()
    print(f"🌍 Environment Detection:")
    print(f"   Platform: {platform.system()} {platform.release()}")
    print(f"   Python: {platform.python_version()}")
    print(f"   Running on Render: {'✅ YES' if is_render else '❌ NO'}")
    
    if is_render:
        print(f"   Render Service: {os.getenv('RENDER_SERVICE_NAME', 'Unknown')}")
        print(f"   Render Instance: {os.getenv('RENDER_INSTANCE_ID', 'Unknown')}")
    
    print(f"   Debug Mode: {'✅ ENABLED' if DEBUG_MODE else '❌ DISABLED'}")
    print(f"   Data Directory: {DATA_DIR}")
    print(f"   Host: {HOST}:{PORT}")

# Detect environment
IS_RENDER = is_running_on_render()

# Load environment variables with validation
try:
    # OAuth Configuration
    CLIENT_ID = get_env_with_fallback("CLIENT_ID", required=True)
    CLIENT_SECRET = get_env_with_fallback("CLIENT_SECRET", required=True)
    REDIRECT_URI = get_env_with_fallback("REDIRECT_URI", required=True)

    # Yandex Payment Configuration
    YANDEX_MERCHANT_ID = get_env_with_fallback("YANDEX_MERCHANT_ID", required=True)
    YANDEX_API_URL = get_env_with_fallback("YANDEX_API_URL", required=True)
    
    # Security
    SECRET_KEY = get_env_with_fallback("SECRET_KEY", required=True)
    adminPassword = get_env_with_fallback("adminPassword", required=True)

    # API Keys
    DADATA_API_TOKEN = get_env_with_fallback("DADATA_API_TOKEN", required=True)
    YANDEX_MAPS_API_KEY = get_env_with_fallback("YANDEX_MAPS_API_KEY", required=True)
    
    print("✅ All required environment variables loaded successfully!")
    
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    if IS_RENDER:
        print("💡 Tip: Make sure to set all required environment variables in your Render dashboard.")
        print("   Go to your service → Environment → Environment Variables")
    else:
        print("💡 Tip: Create a .env file in your project root with all required variables.")
    raise

# Email configuration
EMAIL_USER = get_env_with_fallback("EMAIL_USER", "your-email@yandex.ru")
EMAIL_PASSWORD = get_env_with_fallback("EMAIL_PASSWORD", "your-app-password")
ADMIN_EMAIL = get_env_with_fallback("ADMIN_EMAIL", "admin@samin.ru")

# Server configuration
DEBUG_MODE = get_env_with_fallback("DEBUG_MODE", "True").lower() == "true"
HOST = get_env_with_fallback("HOST", "0.0.0.0")
PORT = int(get_env_with_fallback("PORT", "5000"))

# Email service configuration
SMTP_SERVER = get_env_with_fallback("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(get_env_with_fallback("SMTP_PORT", "587"))

# File paths configuration - adjust for Render if needed
if IS_RENDER:
    # On Render, use absolute paths or environment-specific paths
    DATA_DIR = get_env_with_fallback("DATA_DIR", "/opt/render/project/src/static/data")
    PRIVATE_DIR = get_env_with_fallback("PRIVATE_DIR", "/opt/render/project/src/private")
    UPLOADS_DIR = get_env_with_fallback("UPLOADS_DIR", "/opt/render/project/src/static/uploads")
else:
    # Local development paths
    DATA_DIR = get_env_with_fallback("DATA_DIR", "static/data")
    PRIVATE_DIR = get_env_with_fallback("PRIVATE_DIR", "private")
    UPLOADS_DIR = get_env_with_fallback("UPLOADS_DIR", "static/uploads")

# File upload configuration
MAX_FILE_SIZE = int(get_env_with_fallback("MAX_FILE_SIZE", "5242880"))  # 5MB default
ALLOWED_EXTENSIONS = set(get_env_with_fallback("ALLOWED_EXTENSIONS", "png,jpg,jpeg,gif,webp").split(","))

# Application settings
APP_NAME = get_env_with_fallback("APP_NAME", "Samin")
APP_VERSION = get_env_with_fallback("APP_VERSION", "1.0.0")

# Log environment information when module is imported
if __name__ != "__main__":
    log_environment_info()
