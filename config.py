# Keys,Ids,Tokens,etc.

from dotenv import load_dotenv
import os
import platform
import socket

# Smart environment loading based on environment
def load_environment_variables():
    """Load environment variables from appropriate source"""
    
    # Check if we're on a Linux server (production)
    if platform.system() == "Linux" and os.path.exists("/etc/samin/samin.env"):
        # Production: Load from system environment file
        print("🌐 Production environment detected - loading from /etc/samin/samin.env")
        load_dotenv("/etc/samin/samin.env")
    elif os.path.exists(".env"):
        # Local development: Load from local .env file
        print("💻 Local development detected - loading from .env")
        load_dotenv(".env")
    else:
        # Fallback: Try to load from system environment file if it exists
        if os.path.exists("/etc/samin/samin.env"):
            print("🌐 Loading from system environment file")
            load_dotenv("/etc/samin/samin.env")
        else:
            print("⚠️ No .env file found locally and no system environment file")
            print("   Environment variables must be set manually or via system environment")

# Load environment variables
load_environment_variables()

# Debug: Show what was loaded
print("🔍 Environment Loading Debug:")
print(f"   Platform: {platform.system()}")
print(f"   .env exists: {os.path.exists('.env')}")
print(f"   /etc/samin/samin.env exists: {os.path.exists('/etc/samin/samin.env')}")
print(f"   CLIENT_ID loaded: {'✅' if os.getenv('CLIENT_ID') else '❌'}")
print(f"   adminPassword loaded: {'✅' if os.getenv('adminPassword') else '❌'}")
print(f"   SECRET_KEY loaded: {'✅' if os.getenv('SECRET_KEY') else '❌'}")

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
        # Check what environment files exist
        env_files = []
        if os.path.exists(".env"):
            env_files.append(".env")
        if os.path.exists("/etc/samin/samin.env"):
            env_files.append("/etc/samin/samin.env")
        
        if is_running_on_render():
            raise ValueError(f"Required environment variable {key} not set on Render. Please configure it in your Render dashboard.")
        elif env_files:
            raise ValueError(f"Required environment variable {key} not set. Found environment files: {', '.join(env_files)}")
        else:
            raise ValueError(f"Required environment variable {key} not set. No environment files found.")
    
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
    # Yandex OAuth Configuration
    YANDEX_CLIENT_ID = get_env_with_fallback("YANDEX_CLIENT_ID", "f9d87c4baa2f45f985cf6936b32cb9ea", required=True)
    YANDEX_CLIENT_SECRET = get_env_with_fallback("YANDEX_CLIENT_SECRET", "your-client-secret-here", required=True)
    YANDEX_REDIRECT_URI = get_env_with_fallback("YANDEX_REDIRECT_URI", required=True)
    
    # OAuth Endpoints
    YANDEX_TOKEN_URL = 'https://oauth.yandex.ru/token'
    YANDEX_USER_INFO_URL = 'https://login.yandex.ru/info'
    
    # Scopes for Yandex OAuth
    YANDEX_SCOPES = ['login:info', 'login:email']
    
    # Backward compatibility aliases
    CLIENT_ID = YANDEX_CLIENT_ID
    CLIENT_SECRET = YANDEX_CLIENT_SECRET
    REDIRECT_URI = YANDEX_REDIRECT_URI

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
