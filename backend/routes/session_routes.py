

from flask import Blueprint, request, jsonify

from functools import wraps
from datetime import datetime



from services.session_service import get_sessions_by_therapist, get_session_by_id, get_all_sessions, create_session
from utils.auth_decorator import requires_auth

session_bp = Blueprint('sessions', __name__)

@session_bp.route('/', methods=['POST'])
@requires_auth
def add_session():
    data = request.get_json()

    # validate required fields (excluding 'date' since it's now optional)
    for field in ('gladia_id', 'title', 'patient_id', 'therapist_id'):
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # set date to now if not provided, else try to parse it
    if 'date' in data:
        try:
            date = datetime.fromisoformat(data['date'])
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
    else:
        date = datetime.now()

    print(date)
    session = create_session(
        date=date,
        gladia_id=data['gladia_id'],
        title=data['title'],
        note=data.get('note', ''),
        patient_id=data['patient_id'],
        therapist_id=data['therapist_id']
    )

    return jsonify({'id': str(session.id)}), 201


@session_bp.route('/', methods=['GET'])
@requires_auth
def list_sessions():
    print("OK")
    sessions = get_all_sessions()
    return jsonify([{
        'id': str(s.id),
        'date': s.date.isoformat(),
        'gladia_id': s.gladia_id,
        'title': s.title,
        'note': s.note,
        'patient_id': s.patient_id,
        'therapist_id': s.therapist_id
    } for s in sessions]), 200


@session_bp.route('/<uuid:session_id>', methods=['GET'])
@requires_auth
def get_session(session_id):
    session = get_session_by_id(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    return jsonify({
        'id': str(session.id),
        'date': session.date.isoformat(),
        'gladia_id': session.gladia_id,
        'title': session.title,
        'note': session.note,
        'patient_id': session.patient_id,
        'therapist_id': session.therapist_id
    }), 200



@session_bp.route('/me', methods=['POST'])
@requires_auth
def create_my_session():
    data = request.get_json()
    # required: gladia_id, title, patient_id; date optional
    if 'gladia_id' not in data or 'title' not in data or 'patient_id' not in data:
        return jsonify({"error": "'gladia_id', 'title', and 'patient_id' are required"}), 400

    if 'date' in data:
        try:
            date = datetime.fromisoformat(data['date'])
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
    else:
        date = datetime.now()

    user_payload = request.user_info
    session = create_session(
        date=date,
        gladia_id=data['gladia_id'],
        title=data['title'],
        note=data.get('note', ''),
        patient_id=data['patient_id'],
        therapist_id=user_payload['sub']
    )
    return jsonify({'id': str(session.id)}), 201



@session_bp.route('/me', methods=['GET'])
@requires_auth
def my_session():
    user_payload = request.user_info

    sessions = get_sessions_by_therapist(user_payload["sub"])
    if not sessions:
        return jsonify({'error': 'Session not found'}), 404

    # Define this helper if you haven't already
    def session_to_dict(session):
        return {
            'id': str(session.id),
            'date': session.date.isoformat(),
            'title':session.title,
            'gladia_id': session.gladia_id,
            'note': session.note,
            'patient_id': session.patient_id,
            'therapist_id': session.therapist_id
        }

    sessions_dicts = [session_to_dict(s) for s in sessions]

    return jsonify(sessions_dicts), 200

