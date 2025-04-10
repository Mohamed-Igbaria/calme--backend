import requests
from functools import wraps
from flask import  request, jsonify, current_app

from services.auth_service import decode_token


def fetch_user_info(access_token):
    """Fetch user information from Auth0 using the access token"""
    auth0_domain = current_app.config['AUTH0_DOMAIN']
    url = f"https://{auth0_domain}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Extract token from Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401

        try:
            # Validate and decode token
            payload = decode_token(token)

            request.user = payload  # Store decoded JWT payload in request

            # Fetch additional user info (roles, name, etc.) from Auth0
            user_info = fetch_user_info(token)
            request.user_info = user_info  # Store fetched user info in request

        except Exception as e:
            print(str(e))
            return jsonify({'error': str(e)}), 401

        return f(*args, **kwargs)
    return decorated

