from settings import mongodb_uri, port
from pymongo import MongoClient

client = MongoClient(mongodb_uri, port)
db = client['fastApiCollection']
print('Databse connected successfully')