from flask import Blueprint, jsonify
from datetime import timedelta
from Input import conversation

speech_cadence_bp = Blueprint('SpeechCadence_bp', __name__)

@speech_cadence_bp.route('/SessionTimelineAnalysis/SpeechCadence', methods=['GET'])

def talking_time_min():
    hr, min, sec = map(int, conversation[0]["start_time"].split(":"))
    conv_start = timedelta(hours = hr,minutes=min,seconds=sec)
    hr, min, sec = map(int, conversation[-1]["end_time"].split(":"))
    conv_end = timedelta(hours = hr,minutes=min,seconds=sec)
    client_time = therapist_time = AI_time = timedelta()
    client_words = therapist_words = AI_words = 0

    for elem in conversation:
        hr, min, sec = map(int, elem["start_time"].split(":"))
        start_time = timedelta(hours = hr,minutes=min,seconds=sec)
        hr, min, sec = map(int, elem["end_time"].split(":"))
        end_time = timedelta(hours = hr,minutes=min,seconds=sec)


        message = elem.get("message", "")
        word_count = len(message.strip().split())

        match elem["speaker"]:

            case "Therapist":
                 therapist_time += end_time - start_time
                 therapist_words += word_count
            case "Client":
                 client_time += end_time - start_time
                 client_words += word_count

            case _:
              raise ValueError
            
    therapist_minutes = therapist_time.total_seconds() / 60
    client_minutes = client_time.total_seconds() / 60
    therapist_wpm = therapist_words / therapist_minutes if therapist_minutes > 0 else 0
    client_wpm = client_words / client_minutes if client_minutes > 0 else 0

    talking_time = {
        "Therapist": therapist_time.total_seconds()/60
        ,"therapist_words": therapist_words
        ,"therapist_wpm": round(therapist_wpm, 2)
        ,"Client": client_time.total_seconds()/60
        ,"client_words": client_words
        ,"client_wpm": round(client_wpm, 2)
                   
         }









    return jsonify(talking_time), 200