# utils/__init__.py

import jwt
from datetime import datetime, timedelta
from flask import current_app


def generate_jwt(user_id):
    expiration_time = datetime.utcnow() + timedelta(days=1)

    # Get SECRET_KEY from the current app's config
    secret_key = current_app.config.get('SECRET_KEY')

    if not secret_key:
        raise ValueError("SECRET_KEY not found in app config")

    token = jwt.encode(
        {'user_id': user_id, 'exp': expiration_time},
        secret_key,
        algorithm="HS256"
    )
    return token
