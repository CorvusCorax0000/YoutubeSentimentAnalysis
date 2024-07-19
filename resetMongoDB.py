from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://bigDataUser:userDeUser@bigdataproject.a4fdwdx.mongodb.net/?retryWrites=true&w=majority&appName=BigDataProject')

db = client['youtube_analysis']

collection1 = db['prediction']
collection1.delete_many({})
document1 = {
    "timestamp": 1720145793396,
    "datetime": "2005-06-14 16:45:00",
    "userid": "anon",
    "username": "anon",
    "message": "neutral",
    "predict": ["POSITIVE", 0.555555555555555]
}
collection1.insert_one(document1)

collection0 = db['processed_data']
collection0.delete_many({})
document0 = {
    "NEGATIVE": 0,
    "POSITIVE": 0,
    "TOTAL": 0,
    "POINTS": 0
}
collection0.insert_one(document0)

print("Database is reset.")