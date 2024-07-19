from kafkaHelper import initProducer, produceData
import sys
import pytchat
from pymongo import MongoClient

from sentimentPredict import analyze_sentiment

TOPIC = "prediction"

# VIDEO_ID = sys.argv[2]

client = MongoClient('mongodb+srv://bigDataUser:userDeUser@bigdataproject.a4fdwdx.mongodb.net/?retryWrites=true&w=majority&appName=BigDataProject')
db = client['youtube_analysis']
collection = db['video_ids']

def fetch_latest_video_id():
    # Get the latest video ID based on the timestamp
    video_document = collection.find_one(sort=[('timestamp', -1)])
    video_id = video_document.get('video_id', None) if video_document else None

    return video_id

VIDEO_ID = fetch_latest_video_id()
producer = initProducer()
chat = pytchat.create(video_id=VIDEO_ID)
if(chat.is_alive()):
    print("Livestream chat connected successfully")
    while chat.is_alive():
        for raw_data in chat.get().sync_items():
            data = {
                'timestamp': raw_data.timestamp,
                'datetime': raw_data.datetime,
                'userid': raw_data.id,
                'username': raw_data.author.name,
                'message': raw_data.message,
                'predict': analyze_sentiment(raw_data.message)
            }

            produceData(TOPIC, producer, data)