# Working Yandex OAuth Implementation (adapted from test code)

from flask import Blueprint, redirect, request, session, url_for, flash, render_template, jsonify
import requests
import json
from config import YANDEX_CLIENT_ID, YANDEX_CLIENT_SECRET, YANDEX_REDIRECT_URI, YANDEX_TOKEN_URL, YANDEX_USER_INFO_URL, YANDEX_SCOPES

auth_bp = Blueprint("auth", __name__)

# Main index route is handled by main blueprint

@auth_bp.route("/login")
def login():
    """Initiate Yandex OAuth flow"""
    try:
        # Build OAuth authorization URL
        auth_params = {
            'response_type': 'code',
            'client_id': YANDEX_CLIENT_ID,
            'redirect_uri': YANDEX_REDIRECT_URI,
            'scope': ' '.join(YANDEX_SCOPES)
        }
        
        # Create authorization URL (using the working approach from test code)
        auth_url = f"https://oauth.yandex.ru/authorize?response_type={auth_params['response_type']}&client_id={auth_params['client_id']}&redirect_uri={auth_params['redirect_uri']}&scope={auth_params['scope']}"
        
        print(f"🔐 Redirecting to Yandex OAuth: {auth_url}")
        return redirect(auth_url)
        
    except Exception as e:
        print(f"❌ OAuth Login Error: {str(e)}")
        flash("Ошибка при инициализации входа", "error")
        return redirect(url_for("main.index"))

@auth_bp.route("/auth/callback")
def auth_callback():
    """Handle the OAuth callback from Yandex"""
    try:
        # Get the authorization code from the URL
        code = request.args.get('code')
        error = request.args.get('error')
        
        if error:
            print(f"❌ OAuth Error: {error}")
            return render_template('oauth_error.html', error=f"Authorization error: {error}")
        
        if not code:
            print("❌ No authorization code received")
            return render_template('oauth_error.html', error="No authorization code received")
        
        print(f"✅ Authorization code received: {code[:10]}...")
        
        # Exchange authorization code for access token
        token_response = requests.post(YANDEX_TOKEN_URL, data={
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': YANDEX_CLIENT_ID,
            'client_secret': YANDEX_CLIENT_SECRET,
            'redirect_uri': YANDEX_REDIRECT_URI
        })
        
        if token_response.status_code != 200:
            print(f"❌ Token exchange failed: {token_response.status_code} - {token_response.text}")
            return render_template('oauth_error.html', error=f"Token exchange failed: {token_response.text}")
        
        token_data = token_response.json()
        access_token = token_data.get('access_token')
        
        if not access_token:
            print("❌ No access token received")
            return render_template('oauth_error.html', error="No access token received")
        
        print(f"✅ Access token received: {access_token[:10]}...")
        
        # Store token in session
        session['access_token'] = access_token
        session['token_data'] = token_data
        
        # Get user information
        user_info = get_user_info_from_yandex(access_token)
        
        if not user_info or 'error' in user_info:
            print(f"❌ Failed to get user info: {user_info}")
            return render_template('oauth_error.html', error="Failed to get user information")
        
        # Store user info in session
        session['user'] = {
            'id': user_info.get('id'),
            'login': user_info.get('login'),
            'real_name': user_info.get('real_name'),
            'display_name': user_info.get('display_name'),
            'first_name': user_info.get('first_name'),
            'last_name': user_info.get('last_name'),
            'email': user_info.get('default_email'),
            'avatar': user_info.get('default_avatar_id')
        }
        
        session['just_logged_in'] = True
        session.permanent = True
        
        print(f"✅ User authenticated successfully: {session['user']['login']}")
        flash(f"Добро пожаловать, {session['user']['display_name'] or session['user']['login']}!", "success")
        
        return redirect(url_for("main.index"))
        
    except Exception as e:
        print(f"❌ OAuth Callback Error: {str(e)}")
        return render_template('oauth_error.html', error=str(e))

def get_user_info_from_yandex(access_token):
    """Get user information from Yandex using the access token"""
    try:
        print("👤 Fetching user information from Yandex...")
        
        headers = {'Authorization': f'OAuth {access_token}'}
        response = requests.get(YANDEX_USER_INFO_URL, headers=headers)
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ User info received: {json.dumps(user_info, indent=2)}")
            return user_info
        else:
            print(f"❌ Failed to get user info: {response.status_code} - {response.text}")
            return {'error': f'Failed to get user info: {response.status_code}'}
    except Exception as e:
        print(f"❌ User info error: {str(e)}")
        return {'error': f'Error getting user info: {str(e)}'}

@auth_bp.route("/logout")
def logout():
    """Clear user session"""
    try:
        # Clear OAuth-related session variables
        session.pop("user", None)
        session.pop("just_logged_in", None)
        session.pop("access_token", None)
        session.pop("token_data", None)
        
        print("✅ User logged out successfully")
        flash("Вы успешно вышли из аккаунта", "success")
        
        return redirect(url_for("main.index"))
        
    except Exception as e:
        print(f"❌ Logout Error: {str(e)}")
        flash("Ошибка при выходе", "error")
        return redirect(url_for("main.index"))

@auth_bp.route("/api/config")
def get_config():
    """API endpoint to get OAuth configuration for frontend"""
    try:
        return jsonify({
            'client_id': YANDEX_CLIENT_ID,
            'redirect_uri': YANDEX_REDIRECT_URI,
            'scopes': YANDEX_SCOPES
        })
        
    except Exception as e:
        print(f"❌ OAuth Config Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route("/api/user-info")
def get_user_info():
    """API endpoint to get user information using the stored token"""
    try:
        access_token = session.get('access_token')
        
        if not access_token:
            return jsonify({'error': 'No access token found. Please authenticate first.'}), 401
        
        user_info = get_user_info_from_yandex(access_token)
        return jsonify(user_info)
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route("/api/oauth-status")
def oauth_status():
    """API endpoint to check OAuth status"""
    try:
        has_token = 'access_token' in session
        has_user = 'user' in session
        
        return jsonify({
            'has_token': has_token,
            'has_user': has_user,
            'user': session.get('user'),
            'client_id': YANDEX_CLIENT_ID,
            'redirect_uri': YANDEX_REDIRECT_URI
        })
        
    except Exception as e:
        print(f"❌ OAuth Status Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


