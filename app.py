from flask import Flask, session
from werkzeug.middleware.proxy_fix import ProxyFix
from config import SECRET_KEY, DEBUG_MODE, HOST, PORT, IS_RENDER
from routes.main import main_bp
from routes.auth import auth_bp
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
    
    # CRITICAL: Force these values explicitly
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    print(f"🔒 Production Session Config Applied:")
    print(f"   SESSION_COOKIE_SECURE: {app.config.get('SESSION_COOKIE_SECURE')}")
    print(f"   SESSION_COOKIE_SAMESITE: {app.config.get('SESSION_COOKIE_SAMESITE')}")
    print(f"   SESSION_COOKIE_HTTPONLY: {app.config.get('SESSION_COOKIE_HTTPONLY')}")
    print(f"   SESSION_COOKIE_DOMAIN: {app.config.get('SESSION_COOKIE_DOMAIN')}")
    print(f"   SESSION_COOKIE_PATH: {app.config.get('SESSION_COOKIE_PATH')}")
    
    # Verify the configuration was set correctly
    if app.config.get('SESSION_COOKIE_SAMESITE') != 'None':
        print("❌ CRITICAL ERROR: SESSION_COOKIE_SAMESITE not set to 'None'!")
        print("   This will break OAuth login!")
    else:
        print("✅ SESSION_COOKIE_SAMESITE successfully set to 'None'")
    
    # Additional session configuration for OAuth compatibility
    @app.before_request
    def before_request():
        """Set session as permanent for all requests"""
        session.permanent = True
        session.modified = True

    # Test endpoint to verify session configuration
    @app.route("/test/session-config")
    def test_session_config():
        """Test endpoint to verify session configuration is loaded"""
        config_status = {
            "DEBUG_MODE": DEBUG_MODE,
            "SESSION_COOKIE_SECURE": app.config.get('SESSION_COOKIE_SECURE'),
            "SESSION_COOKIE_HTTPONLY": app.config.get('SESSION_COOKIE_HTTPONLY'),
            "SESSION_COOKIE_SAMESITE": app.config.get('SESSION_COOKIE_SAMESITE'),
            "SESSION_COOKIE_DOMAIN": app.config.get('SESSION_COOKIE_DOMAIN'),
            "SESSION_COOKIE_PATH": app.config.get('SESSION_COOKIE_PATH'),
            "SESSION_COOKIE_MAX_AGE": app.config.get('SESSION_COOKIE_MAX_AGE'),
            "PERMANENT_SESSION_LIFETIME": app.config.get('PERMANENT_SESSION_LIFETIME'),
            "SESSION_REFRESH_EACH_REQUEST": app.config.get('SESSION_REFRESH_EACH_REQUEST'),
            "SESSION_COOKIE_NAME": app.config.get('SESSION_COOKIE_NAME'),
            "SECRET_KEY_SET": bool(app.secret_key)
        }
        
        # Check if OAuth will work
        oauth_compatible = (
            config_status["SESSION_COOKIE_SECURE"] == True and
            config_status["SESSION_COOKIE_SAMESITE"] == "None" and
            config_status["SESSION_COOKIE_HTTPONLY"] == True
        )
        
        return {
            "session_config": config_status,
            "oauth_compatible": oauth_compatible,
            "message": "✅ OAuth will work!" if oauth_compatible else "❌ OAuth will fail!",
            "timestamp": str(datetime.datetime.now())
        }

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
