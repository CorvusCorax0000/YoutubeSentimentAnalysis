from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import time

client = MongoClient(
    'mongodb+srv://bigDataUser:userDeUser@bigdataproject.a4fdwdx.mongodb.net/?retryWrites=true&w=majority&appName=BigDataProject')

def upload_document_to_collection(database_name, collection_name, document):
    db = client[database_name]
    collection = db[collection_name]
    result = collection.insert_one(document)
    return result.inserted_id

def get_data_from_collection(database_name, collection_name):
    db = client[database_name]
    collection = db[collection_name]

    documents = list(collection.find())
    return documents

def count_labels(documents):
    df = pd.DataFrame(documents)
    predict = df['predict']
    labels = df['predict'].apply(
        lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)

    label_counts = labels.value_counts()
    
    total = label_counts.sum()
    
    label_counts_dict = label_counts.to_dict()
    label_counts_dict['TOTAL'] = int(total)
    label_counts_dict['POINTS'] = round(
        label_counts_dict['POSITIVE'] / label_counts_dict['TOTAL'] * 100, 2)
    
    return label_counts_dict

def postProcess():
    documents = get_data_from_collection('youtube_analysis', 'prediction')
    data = count_labels(documents)
    upload_document_to_collection('youtube_analysis', 'processed_data', data)
    return data