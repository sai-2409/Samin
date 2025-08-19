from flask import Flask, session
from werkzeug.middleware.proxy_fix import ProxyFix
from config import SECRET_KEY, DEBUG_MODE, HOST, PORT, IS_RENDER
from routes.main import main_bp
from routes.auth import auth_bp
from routes.pay import pay_bp
from routes.review import review_bp

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

# HTTPS Session Configuration - CRITICAL for production
if not DEBUG_MODE:
    app.config.update(
        SESSION_COOKIE_SECURE=True,      # Only send cookies over HTTPS
        SESSION_COOKIE_HTTPONLY=True,    # Prevent XSS attacks
        SESSION_COOKIE_SAMESITE='Lax',   # CSRF protection
        SESSION_COOKIE_MAX_AGE=3600,     # 1 hour session
        PERMANENT_SESSION_LIFETIME=3600  # 1 hour session
    )
else:
    # Local development settings
    app.config.update(
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax'
    )

# Регистрация маршрутов
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(pay_bp)
app.register_blueprint(review_bp)

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host=HOST, port=PORT)
