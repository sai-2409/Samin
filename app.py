from flask import Flask, session
from werkzeug.middleware.proxy_fix import ProxyFix
from config import SECRET_KEY, DEBUG_MODE, HOST, PORT, IS_RENDER
from routes.main import main_bp
from routes.auth import auth_bp
from routes.pay import pay_bp
from routes.review import review_bp
import platform

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

# Debug: Show what configuration is being loaded
print(f"🔍 App Configuration Debug:")
print(f"   DEBUG_MODE from config: {DEBUG_MODE}")
print(f"   SECRET_KEY set: {bool(SECRET_KEY)}")
print(f"   Platform: {platform.system() if 'platform' in globals() else 'Unknown'}")

# HTTPS Session Configuration - CRITICAL for production
# Force secure sessions for production HTTPS deployment
if not DEBUG_MODE:
    print("🔒 Setting Production Session Configuration...")
    app.config.update(
        SESSION_COOKIE_SECURE=True,      # Only send cookies over HTTPS
        SESSION_COOKIE_HTTPONLY=True,    # Prevent XSS attacks
        SESSION_COOKIE_SAMESITE='None',  # Required for OAuth cross-site redirects
        SESSION_COOKIE_MAX_AGE=3600,     # 1 hour session
        PERMANENT_SESSION_LIFETIME=3600, # 1 hour session
        SESSION_COOKIE_DOMAIN=None,      # Let Flask auto-detect
        SESSION_COOKIE_PATH='/',         # Available on all paths
        SESSION_REFRESH_EACH_REQUEST=True, # Keep session alive
        SESSION_COOKIE_NAME='samin_session' # Custom session name
    )
    
    # Force the configuration to take effect
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    
    print(f"🔒 Production Session Config Applied:")
    print(f"   SESSION_COOKIE_SECURE: {app.config.get('SESSION_COOKIE_SECURE')}")
    print(f"   SESSION_COOKIE_SAMESITE: {app.config.get('SESSION_COOKIE_SAMESITE')}")
    print(f"   SESSION_COOKIE_HTTPONLY: {app.config.get('SESSION_COOKIE_HTTPONLY')}")
    
    # Additional session configuration for OAuth compatibility
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
app.register_blueprint(auth_bp)
app.register_blueprint(pay_bp)
app.register_blueprint(review_bp)

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host=HOST, port=PORT)
