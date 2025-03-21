from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
db = mongo.db  # Reference to the database

# Collection reference
users_collection1= db.doctor

# Sample data (used only for testing)
sample_user=[
    {"doc_id":1,"user_name":"admin","user_password":"admin","user_email":"admin@mail.com"},
     

]


# ✅ Insert Sample Users (Run Once)
if users_collection1.count_documents({}) == 0:
    users_collection1.insert_many(sample_user)


def add_doctor():
    data = request.json
    if not data.get("user_name") or not data.get("user_password") or not data.get("user_email"):
        return jsonify({"error": "Name and password and mail are required"}), 400
    
    last_record = users_collection1.find().sort("_id", -1)

    last_id=last_record[0].get("doc_id")
    new_item={ "doc_id":last_id+1,
            
                "user_name":data["user_name"],
                "user_password":data["user_password"],
                "user_email":data["user_email"]}
    id = users_collection1.insert_one(new_item).inserted_id
    return jsonify({"message": "doctor added", "id": str(id)}), 201


# ✅ 2. Read (GET) - Fetch All users
def get_doctors():
    users = list(users_collection1.find({}, {"_id": 0}))  # Exclude _id field
    return jsonify(users), 200

def find_doctor(user_email):
    users=[]
    users = list(users_collection1.find({"user_email":user_email}, {"_id": 0}))  # Exclude _id field
    if len(users)==0:
        return jsonify({"error":len(users)}), 201
    return jsonify({"error":len(users)}), 202







