# routes/user_routes.py
from flask import Blueprint, request, jsonify
from services.user_service import create_user, get_all_users, get_user_by_id
from utils.auth_decorator import requires_auth

user_bp = Blueprint('users', __name__)

# CREATE user
@user_bp.route('/', methods=['POST'])
@requires_auth
def add_user():
    data = request.get_json()
    try:
        user = create_user(data)
        return jsonify(user_to_dict(user)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# LIST users
@user_bp.route('/', methods=['GET'])
@requires_auth
def list_users():
    users = get_all_users()
    return jsonify([user_to_dict(u) for u in users])

# GET user by sub (id)
@user_bp.route('/<sub>', methods=['GET'])
@requires_auth
def get_user(sub: str):
    user = get_user_by_id(sub)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_to_dict(user))

# Utility function to serialize user
def user_to_dict(user):
    return {
        'sub': user.sub,
        'name': user.name,
        'given_name': user.given_name,
        'family_name': user.family_name,
        'nickname': user.nickname,
        'email': user.email,
        'email_verified': user.email_verified,
        'picture': user.picture,  # MongoDB ImageField (if used)
        'roles': user.roles,
    }
