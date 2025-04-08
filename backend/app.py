from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
import apifun as ap

#Including SessionTimelineAnalysisDashboard files 
from SessionTimelineAnalysisDashboardFolder.TalkingTimeData import talking_time_bp
from SessionTimelineAnalysisDashboardFolder.ClientTenseData import client_tense_bp
# from SessionTimelineAnalysisDashboardFolder.SpeechCadenceData import speech_cadence_bp ///NOT READY YET///
from SessionTimelineAnalysisDashboardFolder.ClientSentimentData import client_sentiment_bp


# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)



# Connecting SessionTimelineAnalysisDashboard routes
app.register_blueprint(talking_time_bp)
app.register_blueprint(client_tense_bp)
# app.register_blueprint(speech_cadence_bp) ///NOT READY YET///
app.register_blueprint(client_sentiment_bp)


# Configure MongoDB Atlas Connection
# Use environment variables
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
port = int(os.getenv("FLASK_RUN_PORT", 5000))  # Default to 8000 if not setmongo = PyMongo(app)
mongo = PyMongo(app)
db = mongo.db  # Reference to the database

# Collection reference
users_collection = db.Users

session_col = db.session 
# ✅ 1. Create (POST) - add New user

@app.route('/session', methods=['POST'])
def add_session():
    data = request.json
    if not data.get("sentiment_analysis") :
        return jsonify({"error": "session data are required"}), 400
    count = session_col.count_documents({})
    if count == 0:
          x=data["sentiment_analysis"]["results"]
           
          new_item={ "session_id":1,
              "doc_id":1,
              "user_id":2,
                
                "results":x,

                
        
                }
          id = session_col.insert_one(new_item).inserted_id
    else:
     last_record = session_col.find().sort("_id", -1)
     last_id=last_record[0].get("session_id")
     x=data["sentiment_analysis"]["results"]
           
     new_item={ "session_id":last_id+1,
              "doc_id":1,
              "user_id":2,
                "results":x
                }
     id = session_col.insert_one(new_item).inserted_id
    return jsonify({"message": "product added", "id": str(id)}), 201

# ✅ 2. Read (GET) - Fetch All users
@app.route('/session', methods=['GET'])
def get_session():
    users = list(session_col.find({}, {"_id": 0}))  # Exclude _id field
    return jsonify(users), 200



@app.route('/doctor', methods=['POST'])
def  add_doc():
    return ap.add_doctor()


# ✅ 2. Read (GET) - Fetch All users
@app.route('/doctor', methods=['GET'])
def get_doc():
   return ap.get_doctors()

@app.route('/doctor/<user_email>', methods=['GET'])
def find_doc(user_email):
   return ap.find_doctor(user_email)
    



# ✅ 1. Create (POST) - add New user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not data.get("user_name") or not data.get("user_password") or not data.get("user_email"):
        return jsonify({"error": "Name and password and mail are required"}), 400
    
    last_record = users_collection.find().sort("_id", -1)

    last_id=last_record[0].get("user_id")
    new_item={ "user_id":last_id+1,
              "doc_id":1,
                
                "user_name":data["user_name"],
                "user_password":data["user_password"],
                "user_email":data["user_email"]}
    id = users_collection.insert_one(new_item).inserted_id
    return jsonify({"message": "product added", "id": str(id)}), 201


# ✅ 2. Read (GET) - Fetch All users
@app.route('/', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))  # Exclude _id field
    return jsonify(users), 200

@app.route('/user/<user_email>', methods=['GET'])
def get_user(user_email):
    users=[]
    users = list(users_collection.find({"user_email":user_email}, {"_id": 0}))  # Exclude _id field
    if len(users)==0:
        return jsonify({"error":len(users)}), 201
    return jsonify({"error":len(users)}), 202

    

@app.route('/find/<user_email>', methods=['GET'])
def find_user(user_email):
    users=[]
    users = list(users_collection.find({"user_email":user_email}, {"_id": 0}))  # Exclude _id field
    if len(users)==0:
        return jsonify({"error":len(users)}), 201
    return jsonify({"error":len(users)}), 202




# ✅ 3. Update (PUT/PATCH) - Update user by id
@app.route('/users/<user_email>', methods=['PUT'])
def update_user(user_email):
    data = request.json
    updated = users_collection.update_one({"user_email": user_email}, {"$set": data})

    if updated.matched_count == 0:
        return jsonify({"error": "user not found"}), 404

    return jsonify({"message": "user updated"}), 200


# ✅ 4. Delete (DELETE) - Remove product by id
@app.route('/users/<user_email>', methods=['DELETE'])
def delete_product(user_email):
    deleted = users_collection.delete_one({"user_email": user_email})

    if deleted.deleted_count == 0:
        return jsonify({"error": "user not found"}), 404

    return jsonify({"message": "user deleted"}), 200




# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
