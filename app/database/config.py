from pymongo import MongoClient
from app.config import MONGO_URL


client = MongoClient(MONGO_URL)

db = client.get_database("API6")

avaliacao_collection = db.get_collection("avaliacao")
