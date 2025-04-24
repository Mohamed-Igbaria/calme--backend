import os
import requests
from flask import Blueprint, request, jsonify
from datetime import datetime

from app import db
from config import Config
from models import Session
from services.session_service import (
    get_sessions_by_therapist,
    get_session_by_id,
    get_all_sessions,
    create_session,
    save_transcription, analyze_transcription_with_gemini, map_names_to_roles, top_words_by_speaker,

)
from utils.auth_decorator import requires_auth

session_bp = Blueprint('sessions', __name__)

@session_bp.route('/', methods=['POST'])
# @requires_auth
def add_session():
    data = request.get_json()

    for field in ( 'title', 'patient_id', 'therapist_id'):
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        date = datetime.fromisoformat(data['date']) if 'date' in data else datetime.now()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    patient_ids = [data['patient_id']]  # wrapping single ID as list

    session = create_session(
        date=date,
        title=data['title'],
        note=data.get('note', ''),
        patient_ids=patient_ids,
        therapist_id=data['therapist_id']
    )

    return jsonify({'id': str(session.id)}), 201


@session_bp.route('/', methods=['GET'])
@requires_auth
def list_sessions():
    sessions = get_all_sessions()
    return jsonify([{
        'id': str(s.id),
        'date': s.date.isoformat(),
        'gladia_id': s.gladia_id,
        'title': s.title,
        'note': s.note,
        'patient_id': [p.id for p in s.patients],
        'therapist_id': s.therapist_id
    } for s in sessions]), 200


@session_bp.route('/<int:session_id>', methods=['GET'])
# @requires_auth
def get_session(session_id):
    # Fetch the session by session_id (now an integer)
    session = Session.query.get(session_id)

    if not session:
        return jsonify({'error': 'Session not found'}), 404

    # Return session data with the necessary fields, including transcription_data, analysis_data, and top_words
    return jsonify({
        'id': session.id,  # Session ID as integer
        'date': session.date.isoformat(),  # Date in ISO format
        'title': session.title,
        'note': session.note,
        'patient_id': [p.id for p in session.patients],  # Patient IDs as a list
        'therapist_id': session.therapist_id,
        'transcription_data': session.transcription_data,  # Including transcription data
        'analysis_data': session.analysis_data,  # Including analysis data
        'top_words': session.top_words  # Including top words
    }), 200


@session_bp.route('/me', methods=['POST'])
@requires_auth
def create_my_session():
    data = request.get_json()
    for field in ('gladia_id', 'title', 'patient_id'):
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        date = datetime.fromisoformat(data['date']) if 'date' in data else datetime.now()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    user_payload = request.user_info
    patient_ids = [data['patient_id']]

    session = create_session(
        date=date,
        gladia_id=data['gladia_id'],
        title=data['title'],
        note=data.get('note', ''),
        patient_ids=patient_ids,
        therapist_id=user_payload['sub']
    )
    return jsonify({'id': str(session.id)}), 201


@session_bp.route('/me', methods=['GET'])
@requires_auth
def my_session():
    user_payload = request.user_info
    sessions = get_sessions_by_therapist(user_payload["sub"])

    def session_to_dict(session):
        return {
            'id': str(session.id),
            'date': session.date.isoformat(),
            'title': session.title,
            'gladia_id': session.gladia_id,
            'note': session.note,
            'patient_id': [p.id for p in session.patients],
            'therapist_id': session.therapist_id
        }

    return jsonify([session_to_dict(s) for s in sessions]), 200


@session_bp.route('/upload-audio/<int:session_id>', methods=['POST'])
@requires_auth
def upload_audio(session_id):
    audio_file = request.files.get("audio")

    if not audio_file:
        return jsonify({"error": "No audio file uploaded"}), 400

    # Prepare the form data and headers
    headers = {
        "xi-api-key": Config.ELEVENLABS_API_KEY,
    }

    files = {
        "file": (audio_file.filename, audio_file.stream, audio_file.mimetype)
    }

    # Add required 'model_id'
    data = {
        "model_id": "scribe_v1"
    }

    # Make the POST request to ElevenLabs
    # response = requests.post(
    #     "https://api.elevenlabs.io/v1/speech-to-text",
    #     headers=headers,
    #     files=files,
    #     data=data
    # )
    #
    # print(response)
    #
    # if response.status_code != 200:
    #     return jsonify({
    #         "error": "Speech-to-text failed",
    #         "details": response.text
    #     }), 500

    # transcription_data = response.json()
    transcription_data = {'language_code': 'eng', 'language_probability': 0.8973588943481445, 'text': "Hello, I'm Sam. What's your name? My name is Pam. Nice to meet you, Pam. Nice to meet you, too.", 'words': [{'text': 'Hello,', 'start': 0.659, 'end': 1.22, 'type': 'word'}, {'text': ' ', 'start': 1.22, 'end': 1.74, 'type': 'spacing'}, {'text': "I'm", 'start': 1.74, 'end': 1.899, 'type': 'word'}, {'text': ' ', 'start': 1.899, 'end': 1.939, 'type': 'spacing'}, {'text': 'Sam.', 'start': 1.939, 'end': 2.379, 'type': 'word'}, {'text': ' ', 'start': 2.379, 'end': 2.859, 'type': 'spacing'}, {'text': "What's", 'start': 2.859, 'end': 3.119, 'type': 'word'}, {'text': ' ', 'start': 3.119, 'end': 3.119, 'type': 'spacing'}, {'text': 'your', 'start': 3.119, 'end': 3.239, 'type': 'word'}, {'text': ' ', 'start': 3.239, 'end': 3.299, 'type': 'spacing'}, {'text': 'name?', 'start': 3.299, 'end': 3.659, 'type': 'word'}, {'text': ' ', 'start': 3.659, 'end': 4.5, 'type': 'spacing'}, {'text': 'My', 'start': 4.5, 'end': 4.719, 'type': 'word'}, {'text': ' ', 'start': 4.719, 'end': 4.779, 'type': 'spacing'}, {'text': 'name', 'start': 4.779, 'end': 5.019, 'type': 'word'}, {'text': ' ', 'start': 5.019, 'end': 5.079, 'type': 'spacing'}, {'text': 'is', 'start': 5.079, 'end': 5.199, 'type': 'word'}, {'text': ' ', 'start': 5.199, 'end': 5.259, 'type': 'spacing'}, {'text': 'Pam.', 'start': 5.259, 'end': 5.699, 'type': 'word'}, {'text': ' ', 'start': 5.699, 'end': 9.659, 'type': 'spacing'}, {'text': 'Nice', 'start': 9.659, 'end': 9.979, 'type': 'word'}, {'text': ' ', 'start': 9.979, 'end': 10.019, 'type': 'spacing'}, {'text': 'to', 'start': 10.019, 'end': 10.119, 'type': 'word'}, {'text': ' ', 'start': 10.119, 'end': 10.139, 'type': 'spacing'}, {'text': 'meet', 'start': 10.139, 'end': 10.319, 'type': 'word'}, {'text': ' ', 'start': 10.319, 'end': 10.359, 'type': 'spacing'}, {'text': 'you,', 'start': 10.359, 'end': 10.679, 'type': 'word'}, {'text': ' ', 'start': 10.679, 'end': 10.92, 'type': 'spacing'}, {'text': 'Pam.', 'start': 10.92, 'end': 11.419, 'type': 'word'}, {'text': ' ', 'start': 11.419, 'end': 12.359, 'type': 'spacing'}, {'text': 'Nice', 'start': 12.359, 'end': 12.699, 'type': 'word'}, {'text': ' ', 'start': 12.699, 'end': 12.739, 'type': 'spacing'}, {'text': 'to', 'start': 12.739, 'end': 12.859, 'type': 'word'}, {'text': ' ', 'start': 12.859, 'end': 12.88, 'type': 'spacing'}, {'text': 'meet', 'start': 12.88, 'end': 13.119, 'type': 'word'}, {'text': ' ', 'start': 13.119, 'end': 13.159, 'type': 'spacing'}, {'text': 'you,', 'start': 13.159, 'end': 13.44, 'type': 'word'}, {'text': ' ', 'start': 13.44, 'end': 13.699, 'type': 'spacing'}, {'text': 'too.', 'start': 13.699, 'end': 14.06, 'type': 'word'}]}



    saved_session = save_transcription(session_id, transcription_data)
    if not saved_session:
        return jsonify({"error": "Session not found"}), 404

    analyzed_data = analyze_transcription_with_gemini(transcription_data)

    name_to_role = map_names_to_roles(analyzed_data)

    # transcription_data["text"] or transcription_data.get("transcript")
    top_words = top_words_by_speaker(transcription_data["text"], name_to_role)



    saved_session.analysis_data = analyzed_data
    saved_session.top_words = top_words
    saved_session.transcription_data = transcription_data
    db.session.commit()

    return jsonify({
        "message": "Uploaded and analyzed successfully",
        "data": {"analyzed_data":analyzed_data,"transcription_data":transcription_data,"top_words":top_words}
    }), 200