from flask import Flask, session
from werkzeug.middleware.proxy_fix import ProxyFix
from config import SECRET_KEY, DEBUG_MODE, HOST, PORT, IS_RENDER
from routes.main import main_bp
# from routes.auth import auth_bp  # OAuth removed
from routes.pay import pay_bp
from routes.review import review_bp
import platform
import datetime

app = Flask(__name__)

# Fix for reverse proxy (nginx/apache) - CRITICAL for HTTPS OAuth
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,      # Trust X-Forwarded-For header
    x_proto=1,    # Trust X-Forwarded-Proto header
    x_host=1,     # Trust X-Forwarded-Host header
    x_prefix=1    # Trust X-Forwarded-Prefix header
)

app.secret_key = SECRET_KEY

# Health check endpoint - always available
@app.get("/__ping")
def ping():
    return "ok"

# Version check endpoint - always available
@app.get("/__version")
def version():
    try:
        import subprocess
        rev = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"]
        ).decode().strip()
    except Exception:
        rev = "unknown"
    return {"status": "ok", "commit": rev}, 200

# Debug: Show what configuration is being loaded
print(f"🔍 App Configuration Debug:")
print(f"   DEBUG_MODE from config: {DEBUG_MODE}")
print(f"   SECRET_KEY set: {bool(SECRET_KEY)}")
print(f"   Platform: {platform.system() if 'platform' in globals() else 'Unknown'}")

# Basic Session Configuration (OAuth removed)
if not DEBUG_MODE:
    print("🔒 Setting Production Session Configuration...")
    app.config.update(
        SESSION_COOKIE_SECURE=True,      # Only send cookies over HTTPS
        SESSION_COOKIE_HTTPONLY=True,    # Prevent XSS attacks
        SESSION_COOKIE_SAMESITE='Lax',   # Standard security setting
        SESSION_COOKIE_MAX_AGE=3600,     # 1 hour session
        PERMANENT_SESSION_LIFETIME=3600, # 1 hour session
        SESSION_COOKIE_DOMAIN=None,      # Let Flask auto-detect
        SESSION_COOKIE_PATH='/',         # Available on all paths
        SESSION_REFRESH_EACH_REQUEST=True, # Keep session alive
        SESSION_COOKIE_NAME='samin_session' # Custom session name
    )
    
    print(f"🔒 Production Session Config Applied:")
    print(f"   SESSION_COOKIE_SECURE: {app.config.get('SESSION_COOKIE_SECURE')}")
    print(f"   SESSION_COOKIE_HTTPONLY: {app.config.get('SESSION_COOKIE_HTTPONLY')}")
    print(f"   SESSION_COOKIE_SAMESITE: {app.config.get('SESSION_COOKIE_SAMESITE')}")
    print(f"   SESSION_COOKIE_DOMAIN: {app.config.get('SESSION_COOKIE_DOMAIN')}")
    print(f"   SESSION_COOKIE_PATH: {app.config.get('SESSION_COOKIE_PATH')}")
    
    # Basic session configuration
    @app.before_request
    def before_request():
        """Set session as permanent for all requests"""
        session.permanent = True
        session.modified = True

else:
    print("💻 Setting Local Development Session Configuration...")
    # Local development settings
    app.config.update(
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_DOMAIN=None,
        SESSION_COOKIE_PATH='/'
    )
    print("💻 Local Development Session Configuration: SECURE=False")

# Регистрация маршрутов
app.register_blueprint(main_bp)
# app.register_blueprint(auth_bp)  # OAuth removed
app.register_blueprint(pay_bp)
app.register_blueprint(review_bp)

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host=HOST, port=PORT)
