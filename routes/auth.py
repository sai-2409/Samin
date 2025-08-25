# Login and Logout routes

from flask import Blueprint, redirect, request, session, url_for, flash
import requests
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    """Simple OAuth login - using the working approach"""
    try:
        print(f"🔐 OAuth Login Started:")
        print(f"   CLIENT_ID: {CLIENT_ID}")
        print(f"   REDIRECT_URI: {REDIRECT_URI}")
        print(f"   DEBUG_MODE: {__debug__}")
        
        # Simple redirect WITHOUT scope to test if that's the issue
        oauth_url = (
            f"https://oauth.yandex.com/authorize?"
            f"response_type=code&"
            f"client_id={CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}"
        )
        
        print(f"🔐 Generated OAuth URL (NO SCOPE): {oauth_url}")
        print(f"🔐 URL Length: {len(oauth_url)}")
        print(f"🔐 Redirecting user to Yandex...")
        
        # Alternative URL with scope for comparison
        oauth_url_with_scope = (
            f"https://oauth.yandex.com/authorize?"
            f"response_type=code&"
            f"client_id={CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}&"
            f"scope=login:info login:email"
        )
        
        print(f"🔐 Alternative URL (with scope): {oauth_url_with_scope}")
        print(f"🔐 Using URL WITHOUT scope: {oauth_url}")
        
        return redirect(oauth_url)
        
    except Exception as e:
        print(f"❌ Login Error: {str(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        flash("Ошибка инициализации входа", "error")
        return redirect(url_for("main.index"))

@auth_bp.route("/callback")
def callback():
    """Simple OAuth callback - using the working approach"""
    try:
        print(f"🔐 OAuth Callback received:")
        print(f"   URL: {request.url}")
        print(f"   Args: {dict(request.args)}")
        
        # Get authorization code
        code = request.args.get("code")
        if not code:
            print("❌ No authorization code received")
            flash("Ошибка авторизации", "error")
            return redirect(url_for("main.index"))

        print(f"✅ Authorization code received: {code[:10]}...")
        
        # Exchange code for access token - SIMPLE VERSION
        print(f"🔐 Exchanging code for access token...")
        token_res = requests.post("https://oauth.yandex.com/token", data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        })
        
        print(f"🔐 Token response status: {token_res.status_code}")
        print(f"🔐 Token response: {token_res.text}")
        
        if token_res.status_code != 200:
            print(f"❌ Token request failed: {token_res.status_code}")
            flash("Ошибка получения токена", "error")
            return redirect(url_for("main.index"))

        token_json = token_res.json()
        access_token = token_json.get("access_token")
        
        if not access_token:
            print(f"❌ No access token in response: {token_json}")
            flash("Токен доступа не получен", "error")
            return redirect(url_for("main.index"))

        print(f"✅ Access token received: {access_token[:10]}...")
        
        # Get user information - SIMPLE VERSION
        print(f"🔐 Getting user information...")
        user_info = requests.get("https://login.yandex.ru/info", headers={
            "Authorization": f"OAuth {access_token}"
        }).json()
        
        print(f"✅ User info received: {user_info.get('login', 'Unknown')}")
        
        # Store user session - SIMPLE VERSION
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
        print(f"✅ Session data: {dict(session)}")
        flash(f"Добро пожаловать, {user_info.get('display_name', user_info['login'])}!", "success")
        
        return redirect(url_for("main.index"))
        
    except Exception as e:
        print(f"❌ Callback Error: {str(e)}")
        flash("Произошла ошибка при входе", "error")
        return redirect(url_for("main.index"))

@auth_bp.route("/logout")
def logout():
    """User logout - only clears user session, preserves admin session"""
    try:
        # Only clear user-related session variables
        session.pop("user", None)
        session.pop("just_logged_in", None)
        
        print("✅ User logged out successfully")
        flash("Вы успешно вышли из аккаунта", "success")
        
        # Do NOT clear admin session
        return redirect(url_for("main.index"))
        
    except Exception as e:
        print(f"❌ Logout Error: {str(e)}")
        return redirect(url_for("main.index"))

@auth_bp.route("/debug/oauth-url")
def debug_oauth_url():
    """Debug endpoint to show exactly what OAuth URL is generated"""
    try:
        # Generate the exact same OAuth URL as the login function
        oauth_url = (
            f"https://oauth.yandex.com/authorize?"
            f"response_type=code&"
            f"client_id={CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}&"
            f"scope=login:info"
        )
        
        debug_info = {
            "generated_oauth_url": oauth_url,
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "full_url_components": {
                "base": "https://oauth.yandex.com/authorize",
                "response_type": "code",
                "client_id": CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "scope": "login:info"
            },
            "yandex_console_checklist": [
                "1. Go to https://oauth.yandex.ru/client",
                "2. Find your app with ID: " + CLIENT_ID,
                "3. Check if status is 'Active'",
                "4. Verify redirect URI matches exactly: " + REDIRECT_URI,
                "5. Ensure scope 'login:info' is allowed"
            ]
        }
        
        return debug_info
        
    except Exception as e:
        return {"error": str(e)}


        # 1. Go to https://oauth.yandex.ru/client
        # 2. Find your app with ID: 23cab000000000000000000000000000
        # 3. Check if status is 'Active'
        # 4. Verify redirect URI matches exactly: https://samin.ru/callback
        # 5. Ensure scope 'login:info' is allowed