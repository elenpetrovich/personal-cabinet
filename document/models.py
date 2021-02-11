from pymongo import MongoClient
from mysite.settings import MONGODB

client = MongoClient(MONGODB)
db_docs = client['documents']