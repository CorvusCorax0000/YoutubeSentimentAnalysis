from transformers import pipeline

# Load pre-trained sentiment analysis model
sentiment_analysis_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
    result = sentiment_analysis_pipeline(text)[0]
    return result['label'], result['score']