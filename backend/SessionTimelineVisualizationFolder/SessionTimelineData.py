from flask import Blueprint, jsonify
from datetime import timedelta
from Input import testData as input_data
import random

session_timeline_visualization_bp = Blueprint('SessionTimelineVisualization_bp', __name__)



def time_to_minutes(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 60 + minutes + seconds / 60

@session_timeline_visualization_bp.route('/SessionTimelineVisualization', methods=['GET'])
def process_session_data():
    conversation = input_data.get('conversation', [])
    if not conversation:
        return {
            'duration': 0,
            'clinicianTalk': [],
            'memberTalk': [],
            'topics': []
        }
    
    first_entry = conversation[0]
    last_entry = conversation[-1]
    session_start = time_to_minutes(first_entry['start_time'])
    session_end = time_to_minutes(last_entry['end_time'])
    session_duration = session_end - session_start

    clinician_segments = []
    member_segments = []
    current_speaker = None
    prev_end = 0

    for entry in conversation:
        start = time_to_minutes(entry['start_time']) - session_start
        end = time_to_minutes(entry['end_time']) - session_start
        new_speaker = 'clinician' if entry['speaker'] == 'Therapist' else 'member'

        # Add silence segment if there's a gap
        if start > prev_end:
            gap_segment = {
                'start': prev_end,
                'end': start,
                'isSilence': True
            }
            if current_speaker == 'clinician':
                clinician_segments.append(gap_segment)
            elif current_speaker == 'member':
                member_segments.append(gap_segment)

        # Add talk segment
        talk_segment = {
            'start': start,
            'end': end,
            'isSilence': False,
            'speaker': new_speaker,
            'timeRange': f"{entry['start_time']} - {entry['end_time']}"
        }

        if new_speaker == 'clinician':
            clinician_segments.append(talk_segment)
        else:
            member_segments.append(talk_segment)

        current_speaker = new_speaker
        prev_end = end

    # Process topics
    topic_segments = []
    topic_color_map = {}
    
    if input_data.get('topics'):
        unique_topics = list({topic['topic_name'] for topic in input_data['topics']})
        num_topics = len(unique_topics)
        
        # Generate distinct colors
        for idx, topic_name in enumerate(unique_topics):
            hue = (idx * (360 / num_topics)) % 360
            saturation = 70 + random.random() * 20  # 70-90%
            lightness = 40 + random.random() * 30   # 40-70%
            topic_color_map[topic_name] = f'hsl({hue:.2f}, {saturation:.2f}%, {lightness:.2f}%)'

        # Create topic segments
        for topic in input_data['topics']:
            topic_start = time_to_minutes(topic['start_time'])
            topic_end = time_to_minutes(topic['end_time'])
            
            if topic_start >= session_start and topic_end <= session_end:
                adj_start = topic_start - session_start
                adj_end = topic_end - session_start
                topic_segments.append({
                    'name': topic['topic_name'],
                    'start': adj_start,
                    'end': adj_end,
                    'timeRange': f"{topic['start_time']} - {topic['end_time']}",
                    'color': topic_color_map[topic['topic_name']]
                })

    # Normalization function
    def normalize(time):
        return (time / session_duration) * 60 if session_duration != 0 else 0

    return {
        'duration': 60,
        'clinicianTalk': [{**s, 'start': normalize(s['start']), 'end': normalize(s['end'])} for s in clinician_segments],
        'memberTalk': [{**s, 'start': normalize(s['start']), 'end': normalize(s['end'])} for s in member_segments],
        'topics': [{**t, 'start': normalize(t['start']), 'end': normalize(t['end'])} for t in topic_segments]
    }