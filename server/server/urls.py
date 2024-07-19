"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from threading import Thread

from pymongo import MongoClient
from datetime import datetime

import json
import base64
import io

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import time

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

def data_processing(data):
    get_value = lambda x: x.get('data', '')
    extract_video_id = lambda url: url.split('v=')[-1].split('&')[0] if 'v=' in url else None
    video_id = extract_video_id(get_value(data))
    print(video_id)
    TOPIC = 'prediction'
    DATABASE = 'youtube_analysis'
    
    client = MongoClient('mongodb+srv://bigDataUser:userDeUser@bigdataproject.a4fdwdx.mongodb.net/?retryWrites=true&w=majority&appName=BigDataProject')
    db = client['youtube_analysis']
    collection = db['video_ids']
    
    collection.insert_one({'video_id': video_id, 'timestamp': datetime.now()})
    # producer(TOPIC, video_id)
    # consumer(TOPIC, DATABASE)


client = MongoClient(
    'mongodb+srv://bigDataUser:userDeUser@bigdataproject.a4fdwdx.mongodb.net/?retryWrites=true&w=majority&appName=BigDataProject')

def upload_document_to_collection(database_name, collection_name, document):
    db = client[database_name]
    collection = db[collection_name]
    result = collection.insert_one(document).inserted_id

    return result

def get_data_from_collection(database_name, collection_name):
    db = client[database_name]
    collection = db[collection_name]

    documents = list(collection.find({}, {'_id': 0}).sort('_id', -1).limit(10))
    return documents

def TimeGen():
    n = 0
    while True:
        yield n
        n += 5

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

def postProcess(request):
    documents = get_data_from_collection('youtube_analysis', 'prediction')
    data = count_labels(documents)
    
    upload_document_to_collection('youtube_analysis', 'processed_data', data)
    
    processed_data = get_data_from_collection('youtube_analysis', 'processed_data')
    # data.pop('_id', None)
    
    df = pd.DataFrame(processed_data)
    # df = full_df.drop('_id', axis=1)

    df.info()
    Time = TimeGen()
    time_values = [next(Time) for _ in range(len(df))]
    df['TIME'] = time_values
    
    plt.figure(figsize=(10, 6))
    
    time_np = df['TIME'].to_numpy()
    points_np = df['POINTS'].to_numpy()

    plt.plot(time_np, points_np, label='Points', marker='o')
    # plt.plot(df['TIME'], df['POINTS'], label='Points', marker='o')
    
    latest_row = df.iloc[-1]
    annotation_text = f"Total: {latest_row['TOTAL']}\nPos: {latest_row['POSITIVE']}\nNeg: {latest_row['NEGATIVE']}"
    plt.annotate(annotation_text,
             xy=(0.05, 0.95),  # Top left corner
             xycoords='axes fraction',
             textcoords="offset points",
             xytext=(0, 10),  # Offset from the specified xy position
             ha='left', va='top')
    
    plt.title('Points and Comments Over Time (Seconds)')
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Points')
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return JsonResponse({'chart': string})

@csrf_exempt
def process(request):
    data = json.loads(request.body)
    print(data)
    
    data_processing(data)
    
    response = {
                'status': 'success',
                'message': 'URL received successfully',
                'data': data
            }
    
    return JsonResponse(response, status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csrf_token/', get_csrf_token, name='csrf_token'),
    path('process/', process),
    path('visualize/', postProcess)
]
