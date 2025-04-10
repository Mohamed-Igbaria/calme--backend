# routes/protected_routes.py
from flask import Blueprint, jsonify, request
from services.user_service import get_or_create_user
from utils.auth_decorator import requires_auth

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/protected', methods=['GET'])
@requires_auth
def protected():
    user_payload = getattr(request, 'user_info', None)

    print(user_payload)

    if not user_payload:
        return jsonify({'error': 'User information not available'}), 400

    try:
        # Get or create the user
        user = get_or_create_user(user_payload)
        return jsonify({
            'message': 'Access granted to protected route',
            'user': {
                'sub': user.sub,
                'email': user.email,
                'name': user.name,
            }
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
