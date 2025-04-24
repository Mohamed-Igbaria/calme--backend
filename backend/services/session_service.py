import json
import os
import re
from collections import Counter


import requests

from app import db
from config import Config
from models.session import Session
from models.patient import Patient

import openai

# OpenAI API key setup
openai.api_key = Config.OPENAI_API_KEY


def create_session(date,  title, note, patient_ids, therapist_id):
    session = Session(
        date=date,
        title=title,
        note=note,
        therapist_id=therapist_id
    )


    session.patients = db.session.query(Patient).filter(Patient.id.in_(patient_ids)).all()

    db.session.add(session)
    db.session.commit()
    return session



def get_all_sessions():
    return Session.query.all()


def get_session_by_id(session_id):
    return Session.query.get(session_id)


# ✅ جلب الجلسات الخاصة بمعالج محدد مع خيارات فرز وترقيم الصفحات
def get_sessions_by_therapist(therapist_id, limit=None, offset=None, order_desc=True):
    query = Session.query.filter_by(therapist_id=therapist_id)

    query = query.order_by(Session.date.desc() if order_desc else Session.date.asc())

    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    return query.all()


# ✅ حفظ نص الجلسة
def save_transcription(session_id, transcription_data):
    session = Session.query.get(session_id)
    if not session:
        return None

    session.transcription_data = transcription_data
    db.session.commit()
    return session


def analyze_transcription_with_gemini(transcription_data):
    # Updated system prompt to request structured JSON output
    system_prompt = (
        "You are an advanced assistant designed to deeply analyze therapy session transcripts and provide a complete, accurate, and structured JSON response.\n\n"
        "Your goal is to extract all useful data and summarize the session in a clear and insightful way. The JSON should include:\n\n"
        "{\n"
        "  \"summary\": {\n"
        "    \"session_summary\": \"<A well-written paragraph summarizing the full session>\"\n"
        "  },\n"
        "  \"entities\": {\n"
        "    \"organizations\": [\"Org1\", \"Org2\", ...],\n"
        "    \"peopleName\": [\n"
        "      {\"name\": \"Sam\", \"type\": \"Patient\"},\n"
        "      {\"name\": \"Pam\", \"type\": \"Therapist\"},\n"
        "      ...\n"
        "    ]\n"
        "  },\n"
        "  \"topics\": [\n"
        "    {\n"
        "      \"topic\": \"<Topic name, e.g., Introductions, Goal Setting, CBT Techniques>\",\n"
        "      \"start\": \"00:00:00\",\n"
        "      \"end\": \"00:02:30\",\n"
        "      \"description\": \"<Short explanation of what was discussed>\"\n"
        "    },\n"
        "    ...\n"
        "  ],\n"
        "  \"insights\": {\n"
        "    \"patient_emotion\": \"<Brief insight on patient's emotional state>\",\n"
        "    \"therapist_approach\": \"<Insight into how the therapist guided the session>\",\n"
        "    \"techniques_used\": [\"CBT\", \"Reflective Listening\", ...]\n"
        "  }\n"
        "}\n\n"
        "Important instructions:\n"
        "- Include timestamps (start and end) for each topic.\n"
        "- Output valid raw JSON only — no Markdown, no explanation, no code fences.\n"
        "- You can take your time and be thorough. Accuracy and insight are more important than speed.\n"
    )

    # Set up the Gemini API URL and key
    gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    gemini_api_key = Config.GEMINI_API_KEY  # Assuming you have the Gemini API key stored in your environment variables

    # Prepare the request body with the system prompt and transcription data
    data = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt},
                    {"text": f"Transcript:\n{transcription_data}"}
                ]
            }
        ]
    }

    # Set up the headers for the request
    headers = {
        "Content-Type": "application/json"
    }
    # print(top_words_by_speaker(transcription_data))
    # Make the POST request to the Gemini API
    response = requests.post(f"{gemini_api_url}?key={gemini_api_key}", json=data, headers=headers)

    try:
        # Extract the JSON string from the response
        gemini_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        clean_text = re.sub(r"^```json\s*|\s*```$", "", gemini_text.strip(), flags=re.DOTALL)
        parsed_json = json.loads(clean_text)

        return parsed_json
    except Exception as e:
        return {
            "error": "Failed to parse JSON from Gemini response",
            "details": str(e),
            "raw_response": response.text
        }



def map_names_to_roles(gemini_data):
    name_to_role = {}
    people = gemini_data.get("data", {}).get("entities", {}).get("peopleName", [])
    for person in people:
        name = person["name"]
        role = person["type"]
        name_to_role[name] = role
    return name_to_role

def extract_speaker_dialogue(transcription_data):
    dialogues = {}

    if isinstance(transcription_data, dict):
        transcription_text = transcription_data.get("transcript", "")
    elif isinstance(transcription_data, str):
        transcription_text = transcription_data
    else:
        raise ValueError("Invalid transcription data format")

    sentences = re.split(r'(?<=\.)\s+', transcription_text)
    current_speaker = "Unknown"

    for sentence in sentences:
        match = re.search(r"(?:I['’]m|My name is)\s+([A-Z][a-zA-Z]*)", sentence)
        if match:
            current_speaker = match.group(1).rstrip(".")
            if current_speaker not in dialogues:
                dialogues[current_speaker] = []
        dialogues.setdefault(current_speaker, []).append(sentence)

    return dialogues

def top_words_by_speaker(transcription_text, name_to_role=None, top_n=10):
    dialogues = extract_speaker_dialogue(transcription_text)
    top_words = {}

    for speaker_name, sentences in dialogues.items():
        role = name_to_role.get(speaker_name, speaker_name) if name_to_role else speaker_name
        speaker_text = " ".join(sentences)
        words = re.findall(r'\b\w+\b', speaker_text.lower())
        counts = Counter(words)
        top_words[role] = counts.most_common(top_n)

    return top_words
