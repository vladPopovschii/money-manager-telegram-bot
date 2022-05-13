from pymongo import MongoClient

def init_mongo_client(connection_uri: str) -> MongoClient: 
    mongo_client = MongoClient(connection_uri)
    return mongo_client



