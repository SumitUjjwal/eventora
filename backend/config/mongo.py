from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

mongo = MongoClient(MONGO_URI)

db = mongo['Eventora']