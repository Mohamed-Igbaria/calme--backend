import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Database:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        print("connected to DB!")

    def get_collection(self, name):
        return self.db[name]

    def insert_document(self, collection_name, data: dict):
        collection = self.get_collection(collection_name)
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def fetch_all(self, collection_name):
        collection = self.get_collection(collection_name)
        return list(collection.find())

    def find_one(self, collection_name, query: dict):
        collection = self.get_collection(collection_name)
        return collection.find_one(query)
    
    def find_by_id(self, collection_name, session_id):
        return self.get_collection(collection_name).find_one({"session_id": session_id})
