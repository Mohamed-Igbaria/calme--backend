# transcripts_bp.py

from flask import Blueprint, request, jsonify
from extensions import mongo
from flask_cors import cross_origin
import json
from datetime import datetime
import uuid
import logging
import requests

transcript_bp = Blueprint('transcripts', __name__)
logger = logging.getLogger('transcripts_bp')

@transcript_bp.route('/api/transcript/save', methods=['POST'])
@cross_origin(origins="http://localhost:5173", methods=["POST","OPTIONS"], allow_headers=["Content-Type"])
def save_transcript():
    try:
        # Get data from request
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        required_fields = ['session_id', 'therapist_id', 'user_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create base transcript document
        transcript_doc = {
            "session_id": data['session_id'],
            "therapist_id": data['therapist_id'],  # Using therapist_id instead of doc_id
            "user_id": data['user_id'],
            "created_at": datetime.utcnow(),
            "language": data.get('language', 'en'),
        }

        # Store the complete Gladia response
        gladia_response = data.get('gladia_response')
        
        if gladia_response:
            # Extract and structure the response data
            transcript_doc['gladia_id'] = gladia_response.get('id')
            transcript_doc['request_id'] = gladia_response.get('request_id')
            transcript_doc['status'] = gladia_response.get('status')
            transcript_doc['created_at_gladia'] = gladia_response.get('created_at')
            transcript_doc['completed_at'] = gladia_response.get('completed_at')
            
            # Store file info if available
            if 'file' in gladia_response:
                transcript_doc['file'] = {
                    'id': gladia_response['file'].get('id'),
                    'filename': gladia_response['file'].get('filename'),
                    'audio_duration': gladia_response['file'].get('audio_duration'),
                    'number_of_channels': gladia_response['file'].get('number_of_channels')
                }
            
            # Store request parameters
            if 'request_params' in gladia_response:
                transcript_doc['request_params'] = gladia_response['request_params']
            
            # Process transcription results
            if 'result' in gladia_response and 'transcription' in gladia_response['result']:
                transcription = gladia_response['result']['transcription']
                
                # Store full transcript if available
                if 'full_transcript' in transcription:
                    transcript_doc['full_transcript'] = transcription['full_transcript']
                
                # Store detailed results (utterances or segments)
                if 'utterances' in transcription:
                    transcript_doc['results'] = transcription['utterances']
                elif 'segments' in transcription:
                    transcript_doc['results'] = transcription['segments']
                
                # Add sentiment analysis if available
                if 'sentiment_analysis' in gladia_response['result']:
                    transcript_doc['sentiment_analysis'] = gladia_response['result']['sentiment_analysis']
                
                # Add summarization if available
                if 'summarization' in gladia_response['result']:
                    transcript_doc['summarization'] = gladia_response['result']['summarization']
                
                # Add LLM results if available
                if 'audio_to_llm' in gladia_response['result']:
                    transcript_doc['audio_to_llm'] = gladia_response['result']['audio_to_llm']
            
            # If we can't extract structured data, store the raw response
            if 'results' not in transcript_doc and gladia_response:
                transcript_doc['raw_response'] = gladia_response
        else:
            # If no Gladia response, check for text
            if 'text' in data:
                transcript_doc['full_transcript'] = data['text']
                
                # Create a simple segment
                transcript_doc['results'] = [{
                    "text": data['text'],
                    "language": data.get('language', 'en'),
                    "start": 0,
                    "end": len(data['text']) / 10,  # Rough estimate of duration
                    "speaker": 0,
                    "channel": 0
                }]

        try:
            result = mongo.db.transcripts.insert_one(transcript_doc)
        except Exception as e:
            transcript_bp.logger.error("DB insert failed: %s", e)
            return jsonify({"error": "Database error"}), 500
        return jsonify({
            "message": "Transcript saved successfully",
            "transcript_id": str(result.inserted_id),
            "session_id": data['session_id']
        }), 200

    except Exception as e:
        logger.error(f"Save transcript error: {e}")
        return jsonify({"error": str(e)}), 500

@transcript_bp.route('/api/transcript/<session_id>', methods=['GET'])
def get_transcript(session_id):
    try:
        mongo = current_app.extensions['pymongo']
        
        # Find transcript by session_id
        transcript = mongo.db.session.find_one({"session_id": session_id})
        
        if not transcript:
            return jsonify({"error": "Transcript not found"}), 404
            
        # Convert ObjectId to string for JSON serialization
        transcript['_id'] = str(transcript['_id'])
        
        return jsonify(transcript), 200

    except Exception as e:
        logger.error(f"Get transcript error: {e}")
        return jsonify({"error": str(e)}), 500

@transcript_bp.route('/api/transcripts/by-therapist/<therapist_id>', methods=['GET'])
def get_therapist_transcripts(therapist_id):
    try:
        mongo = current_app.extensions['pymongo']
        
        # Find all transcripts for a therapist
        transcripts = list(mongo.db.session.find({"therapist_id": therapist_id}))
        
        # Convert ObjectId to string for JSON serialization
        for transcript in transcripts:
            transcript['_id'] = str(transcript['_id'])
        
        return jsonify(transcripts), 200

    except Exception as e:
        logger.error(f"Get therapist transcripts error: {e}")
        return jsonify({"error": str(e)}), 500

@transcript_bp.route('/api/transcripts/by-user/<user_id>', methods=['GET'])
def get_user_transcripts(user_id):
    try:
        mongo = current_app.extensions['pymongo']
        
        # Find all transcripts for a user
        transcripts = list(mongo.db.session.find({"user_id": user_id}))
        
        # Convert ObjectId to string for JSON serialization
        for transcript in transcripts:
            transcript['_id'] = str(transcript['_id'])
        
        return jsonify(transcripts), 200

    except Exception as e:
        logger.error(f"Get user transcripts error: {e}")
        return jsonify({"error": str(e)}), 500

@transcript_bp.route('/api/transcript/status/<job_id>', methods=['GET'])
def get_transcript_status(job_id):
    try:
        mongo = current_app.extensions['pymongo']
        GLADIA_API_KEY = current_app.config['GLADIA_API_KEY']
        
        # 1. Check MongoDB first
        transcript = mongo.db.session.find_one({"gladia_id": job_id})
        
        if transcript and transcript.get("status") == "done":
            return jsonify({
                "status": "completed",
                "transcript": transcript.get("full_transcript"),
                "segments": transcript.get("results"),
                "sentiment_analysis": transcript.get("sentiment_analysis"),
                "summarization": transcript.get("summarization"),
                "audio_to_llm": transcript.get("audio_to_llm")
            }), 200

        # 2. Check Gladia status if not complete
        status_response = requests.get(
            f"https://api.gladia.io/v2/pre-recorded/{job_id}",
            headers={"x-gladia-key": GLADIA_API_KEY}
        )
        
        status_data = status_response.json()
        
        if status_data['status'] == 'done':
            # Extract data from Gladia response
            transcript_data = {
                "gladia_id": status_data.get('id'),
                "request_id": status_data.get('request_id'),
                "status": status_data.get('status'),
                "created_at_gladia": status_data.get('created_at'),
                "completed_at": status_data.get('completed_at'),
                "updated_at": datetime.utcnow()
            }
            
            # Extract transcription data
            if 'result' in status_data and 'transcription' in status_data['result']:
                transcription = status_data['result']['transcription']
                
                if 'full_transcript' in transcription:
                    transcript_data['full_transcript'] = transcription['full_transcript']
                
                if 'utterances' in transcription:
                    transcript_data['results'] = transcription['utterances']
                elif 'segments' in transcription:
                    transcript_data['results'] = transcription['segments']
                
                # Add additional results if available
                if 'sentiment_analysis' in status_data['result']:
                    transcript_data['sentiment_analysis'] = status_data['result']['sentiment_analysis']
                
                if 'summarization' in status_data['result']:
                    transcript_data['summarization'] = status_data['result']['summarization']
                
                if 'audio_to_llm' in status_data['result']:
                    transcript_data['audio_to_llm'] = status_data['result']['audio_to_llm']
            
            # Update MongoDB if we found a record
            if transcript:
                mongo.db.session.update_one(
                    {"gladia_id": job_id},
                    {"$set": transcript_data}
                )
            
            return jsonify({
                "status": "completed",
                "transcript": transcript_data.get('full_transcript'),
                "segments": transcript_data.get('results'),
                "sentiment_analysis": transcript_data.get('sentiment_analysis'),
                "summarization": transcript_data.get('summarization'),
                "audio_to_llm": transcript_data.get('audio_to_llm')
            }), 200
            
        return jsonify({
            "status": status_data.get('status'),
            "progress": status_data.get('progress', 0)
        }), 200

    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return jsonify({"error": "Status check failed"}), 500