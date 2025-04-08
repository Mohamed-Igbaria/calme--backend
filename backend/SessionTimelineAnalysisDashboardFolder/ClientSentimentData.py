from flask import Blueprint, jsonify
from Input import conversation

client_sentiment_bp = Blueprint('ClientSentiment_bp', __name__)

@client_sentiment_bp.route('/SessionTimelineAnalysis/ClientSentiment', methods=['GET'])
def Client_sentiment_Extract(): 
    positive_counter = 0
    neutral_counter = 0
    negative_counter = 0
    client_counter = 0
    for elem in conversation :
        
        if elem["speaker"] != "Client":
            continue
        
        client_counter+=1
        match elem["sentiment"]:

            case "Positive":
                 positive_counter+=1

            case "Neutral":
                 neutral_counter+=1

            case "Negative":
                 negative_counter+=1

            case _:
                raise ValueError
        


    output = {
        "positive_counter" : (positive_counter/client_counter),
        "neutral_counter" : (neutral_counter/client_counter),
        "negative_counter" : (negative_counter/client_counter)
    }


    return jsonify(output), 200