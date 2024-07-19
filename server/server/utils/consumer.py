import sys
from dotenv import load_dotenv
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from kafkaHelper import consumeData, initConsumer

import matplotlib.pyplot as plt
import pandas as pd

# from postProcess import postProcess


TOPIC = 'prediction'
DATABASE = 'youtube_analysis'
print('Starting Apache Kafka consumers')
consumer = initConsumer(TOPIC)


load_dotenv()
uri = os.environ['MONGODB_URI']

client = MongoClient(uri)
db = client[DATABASE]
collection = db[TOPIC]

while True:
    records = consumeData(consumer)
    for r in records:
        print(r)
        # postProcess()
        collection.insert_one(r).inserted_id



# # TOPIC = sys.argv[1]
# DATABASE = 'bigDataDemo'
# # print('Starting Apache Kafka consumers')
# # consumer = initConsumer(TOPIC)


# # load_dotenv()
# # uri = os.environ['MONGODB_URI']

# # client = MongoClient(uri)
# # db = client[DATABASE]
# # collection = db[TOPIC]

# def consumer(TOPIC, DATABASE):
    
#     load_dotenv()
#     uri = os.environ['MONGODB_URI']

#     client = MongoClient(uri)
#     db = client[DATABASE]
#     collection = db[TOPIC]
    
#     print('Starting Apache Kafka consumers')
#     consumer = initConsumer(TOPIC)
#     while True:
#         records = consumeData(consumer)
#         for r in records:
#             print(r)
#             collection.insert_one(r).inserted_id
