# Login and Logout routes

from flask import Blueprint, redirect, request, session, url_for, flash
import requests
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    """Simple OAuth login - using the working approach"""
    try:
        # Simple redirect without complex parameters
        oauth_url = (
            f"https://oauth.yandex.com/authorize?"
            f"response_type=code&"
            f"client_id={CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}"
        )
        
        print(f"🔐 Simple OAuth Login URL: {oauth_url}")
        print(f"🔐 CLIENT_ID: {CLIENT_ID}")
        print(f"🔐 REDIRECT_URI: {REDIRECT_URI}")
        
        return redirect(oauth_url)
        
    except Exception as e:
        print(f"❌ Login Error: {str(e)}")
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