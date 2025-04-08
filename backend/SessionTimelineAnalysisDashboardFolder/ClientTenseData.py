from flask import Blueprint, jsonify
from Input import conversation
from SessionTimelineAnalysisDashboardFolder.sentence_tense_extract import detect_future

client_tense_bp = Blueprint('ClientTense_bp', __name__)

@client_tense_bp.route('/SessionTimelineAnalysis/ClientTense', methods=['GET'])
def Client_tense_Extract(): 
    counter = 0
    client_counter = 0
    for elem in conversation :
        
        if elem["speaker"] != "Client":
            continue
        
        client_counter+=1

        isFuture = detect_future(elem["message"])
        if isFuture:
            counter+=1
        
        

    output = {
        "Future_Percentage" : (counter/client_counter)
    }


    return jsonify(output), 200