# Login and Logout routes

from flask import Blueprint, redirect, request, session, url_for
import requests
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    return redirect(
        f"https://oauth.yandex.com/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    )

@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Ошибка авторизации"

    token_res = requests.post("https://oauth.yandex.com/token", data={
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    token_json = token_res.json()
    access_token = token_json.get("access_token")
    if not access_token:
        return "Ошибка получения токена"

    user_info = requests.get("https://login.yandex.ru/info", headers={
        "Authorization": f"OAuth {access_token}"
    }).json()

    session["user"] = {
        "login": user_info["login"],
        "avatar": user_info.get("default_avatar_id"),
        "real_name": user_info.get("real_name"),
        "display_name": user_info.get("display_name"),
        "default_avatar_id": user_info.get("default_avatar_id")
    }
    session["just_logged_in"] = True
    return redirect(url_for("main.index"))

@auth_bp.route("/logout")
def logout():
    # Clear both admin and user sessions
    session.pop("logged_in", None)
    session.pop("user", None)
    session.pop("just_logged_in", None)
    return redirect(url_for("main.index"))
