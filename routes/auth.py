# Basic user session management (OAuth removed)

from flask import Blueprint, redirect, request, session, url_for, flash
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    """Simple login redirect - OAuth removed"""
    flash("Функция входа временно недоступна", "error")
    return redirect(url_for("main.index"))

@auth_bp.route("/callback")
def callback():
    """OAuth callback removed"""
    flash("Функция входа временно недоступна", "error")
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
        flash("Ошибка при выходе", "error")
        return redirect(url_for("main.index"))

@auth_bp.route("/debug/oauth-url")
def debug_oauth_url():
    """OAuth debug endpoint removed"""
    return {"message": "OAuth functionality removed", "status": "disabled"}


