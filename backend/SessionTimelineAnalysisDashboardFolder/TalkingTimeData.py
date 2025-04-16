from flask import Blueprint, jsonify
from datetime import timedelta
from Input import conversation

talking_time_bp = Blueprint('TalkingTime_bp', __name__)

@talking_time_bp.route('/SessionTimelineAnalysis/TalkingTime', methods=['GET'])
def Talking_Time_Extract():
    hr, min, sec = map(int, conversation[0]["start_time"].split(":"))
    conv_start = timedelta(hours = hr,minutes=min,seconds=sec)
    hr, min, sec = map(int, conversation[-1]["end_time"].split(":"))
    conv_end = timedelta(hours = hr,minutes=min,seconds=sec)
    client_time = therapist_time = AI_time = timedelta()
    
    for elem in conversation:
        hr, min, sec = map(int, elem["start_time"].split(":"))
        start_time = timedelta(hours = hr,minutes=min,seconds=sec)
        hr, min, sec = map(int, elem["end_time"].split(":"))
        end_time = timedelta(hours = hr,minutes=min,seconds=sec)
        
        match elem["speaker"]:

            case "Therapist":
                 therapist_time += end_time - start_time

            case "Client":
                 client_time += end_time - start_time

            case "AI":
                 AI_time += end_time - start_time

            case _:
                raise ValueError

    talking_time = {
        "Therapist": therapist_time.total_seconds()
        ,"Client": client_time.total_seconds()
        ,"AI": AI_time.total_seconds()
        ,"Silence": ((conv_end-conv_start) - (therapist_time + client_time + AI_time)).total_seconds()
        ,"Conversation":(conv_end-conv_start).total_seconds()
    }

    return jsonify(talking_time), 200
