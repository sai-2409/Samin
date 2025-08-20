# Login and Logout routes

from flask import Blueprint, redirect, request, session, url_for, current_app, flash
import requests
import secrets
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import traceback
import datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    try:
        # Generate CSRF token for OAuth security
        csrf_token = secrets.token_urlsafe(32)
        session['oauth_csrf_token'] = csrf_token
        
        # Build OAuth URL with state parameter for CSRF protection
        oauth_url = (
            f"https://oauth.yandex.com/authorize?"
            f"response_type=code&"
            f"client_id={CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}&"
            f"state={csrf_token}"
        )
        
        print(f"🔐 OAuth Login URL: {oauth_url}")
        print(f"🔐 Redirect URI: {REDIRECT_URI}")
        print(f"🔐 Client ID: {CLIENT_ID}")
        
        return redirect(oauth_url)
        
    except Exception as e:
        print(f"❌ Login Error: {str(e)}")
        print(f"❌ Traceback: {traceback.format_exc()}")
        flash("Ошибка инициализации входа", "error")
        return redirect(url_for("main.index"))

@auth_bp.route("/callback")
def callback():
    try:
        print(f"🔐 OAuth Callback received:")
        print(f"   URL: {request.url}")
        print(f"   Args: {dict(request.args)}")
        print(f"   Session: {dict(session)}")
        print(f"   Cookies: {dict(request.cookies)}")
        
        # Verify CSRF token
        csrf_token = request.args.get("state")
        stored_token = session.get('oauth_csrf_token')
        
        if not csrf_token or not stored_token or csrf_token != stored_token:
            print(f"❌ CSRF Token Mismatch: received={csrf_token}, stored={stored_token}")
            flash("Ошибка безопасности при входе", "error")
            return redirect(url_for("main.index"))
        
        # Clear CSRF token after use
        session.pop('oauth_csrf_token', None)
        
        # Get authorization code
        code = request.args.get("code")
        if not code:
            print("❌ No authorization code received")
            flash("Код авторизации не получен", "error")
            return redirect(url_for("main.index"))

        print(f"✅ Authorization code received: {code[:10]}...")
        
        # Exchange code for access token
        token_response = requests.post("https://oauth.yandex.com/token", data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI  # Must match exactly
        })
        
        print(f"🔐 Token response status: {token_response.status_code}")
        print(f"🔐 Token response: {token_response.text}")
        
        if token_response.status_code != 200:
            print(f"❌ Token request failed: {token_response.status_code} - {token_response.text}")
            flash("Ошибка получения токена доступа", "error")
            return redirect(url_for("main.index"))

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            print(f"❌ No access token in response: {token_data}")
            flash("Токен доступа не получен", "error")
            return redirect(url_for("main.index"))

        print(f"✅ Access token received: {access_token[:10]}...")
        
        # Get user information
        user_response = requests.get("https://login.yandex.ru/info", headers={
            "Authorization": f"OAuth {access_token}"
        })
        
        if user_response.status_code != 200:
            print(f"❌ User info request failed: {user_response.status_code}")
            flash("Ошибка получения информации о пользователе", "error")
            return redirect(url_for("main.index"))

        user_info = user_response.json()
        print(f"✅ User info received: {user_info.get('login', 'Unknown')}")
        
        # Store user session
        session["user"] = {
            "login": user_info["login"],
            "avatar": user_info.get("default_avatar_id"),
            "real_name": user_info.get("real_name"),
            "display_name": user_info.get("display_name"),
            "default_avatar_id": user_info.get("default_avatar_id")
        }
        session["just_logged_in"] = True
        
        # Make session permanent for HTTPS
        session.permanent = True
        
        print(f"✅ User {user_info['login']} successfully logged in")
        flash(f"Добро пожаловать, {user_info.get('display_name', user_info['login'])}!", "success")
        
        return redirect(url_for("main.index"))
        
    except Exception as e:
        print(f"❌ Callback Error: {str(e)}")
        print(f"❌ Traceback: {traceback.format_exc()}")
        flash("Произошла ошибка при входе", "error")
        return redirect(url_for("main.index"))

@auth_bp.route("/logout")
def logout():
    """User logout - only clears user session, preserves admin session"""
    try:
        # Only clear user-related session variables
        session.pop("user", None)
        session.pop("just_logged_in", None)
        session.pop("oauth_csrf_token", None)
        
        print("✅ User logged out successfully")
        flash("Вы успешно вышли из аккаунта", "success")
        
        # Do NOT clear admin session
        return redirect(url_for("main.index"))
        
    except Exception as e:
        print(f"❌ Logout Error: {str(e)}")
        return redirect(url_for("main.index"))

@auth_bp.route("/debug/oauth")
def debug_oauth():
    """Debug endpoint to check OAuth configuration"""
    # Allow debug in production for troubleshooting
    debug_info = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "has_client_secret": bool(CLIENT_SECRET),
        "session_secure": current_app.config.get('SESSION_COOKIE_SECURE'),
        "session_httponly": current_app.config.get('SESSION_COOKIE_HTTPONLY'),
        "session_samesite": current_app.config.get('SESSION_COOKIE_SAMESITE'),
        "request_scheme": request.scheme,
        "request_host": request.host,
        "request_url": request.url,
        "forwarded_proto": request.headers.get('X-Forwarded-Proto'),
        "forwarded_host": request.headers.get('X-Forwarded-Host'),
        "user_agent": request.headers.get('User-Agent'),
        "session_data": dict(session),
        "cookies": dict(request.cookies)
    }
    
    return debug_info

@auth_bp.route("/test/oauth")
def test_oauth():
    """Test endpoint to manually test OAuth flow"""
    try:
        # Test 1: Check environment variables
        env_check = {
            "CLIENT_ID": CLIENT_ID,
            "REDIRECT_URI": REDIRECT_URI,
            "HAS_CLIENT_SECRET": bool(CLIENT_SECRET),
            "CLIENT_SECRET_LENGTH": len(CLIENT_SECRET) if CLIENT_SECRET else 0
        }
        
        # Test 2: Check current session
        session_check = {
            "has_oauth_csrf_token": 'oauth_csrf_token' in session,
            "oauth_csrf_token": session.get('oauth_csrf_token'),
            "has_user": 'user' in session,
            "user_data": session.get('user'),
            "session_id": session.get('_id', 'No session ID')
        }
        
        # Test 3: Check request headers
        header_check = {
            "scheme": request.scheme,
            "host": request.host,
            "url": request.url,
            "x_forwarded_proto": request.headers.get('X-Forwarded-Proto'),
            "x_forwarded_host": request.headers.get('X-Forwarded-Host'),
            "user_agent": request.headers.get('User-Agent')
        }
        
        # Test 4: Check app config
        config_check = {
            "debug_mode": current_app.debug,
            "session_secure": current_app.config.get('SESSION_COOKIE_SECURE'),
            "session_httponly": current_app.config.get('SESSION_COOKIE_HTTPONLY'),
            "session_samesite": current_app.config.get('SESSION_COOKIE_SAMESITE'),
            "secret_key_set": bool(current_app.secret_key)
        }
        
        return {
            "environment": env_check,
            "session": session_check,
            "headers": header_check,
            "config": config_check,
            "timestamp": str(datetime.datetime.now())
        }
        
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

@auth_bp.route("/simulate/oauth")
def simulate_oauth():
    """Simulate OAuth flow for testing"""
    try:
        # Generate a test CSRF token
        csrf_token = secrets.token_urlsafe(32)
        session['oauth_csrf_token'] = csrf_token
        
        # Simulate the callback with test data
        test_code = "test_auth_code_12345"
        
        print(f"🧪 Simulating OAuth flow:")
        print(f"   Generated CSRF token: {csrf_token}")
        print(f"   Test auth code: {test_code}")
        print(f"   Session before: {dict(session)}")
        
        # Simulate the callback process
        if 'oauth_csrf_token' in session:
            stored_token = session.pop('oauth_csrf_token')
            print(f"   CSRF token verified: {stored_token}")
            
            # Simulate successful login
            session["user"] = {
                "login": "test_user",
                "avatar": "test_avatar",
                "real_name": "Test User",
                "display_name": "Test User",
                "default_avatar_id": "test_avatar"
            }
            session["just_logged_in"] = True
            session.permanent = True
            
            print(f"   Session after: {dict(session)}")
            
            return {
                "status": "success",
                "message": "OAuth simulation completed",
                "session_data": dict(session),
                "csrf_token": stored_token
            }
        else:
            return {
                "status": "error",
                "message": "No CSRF token found in session"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
