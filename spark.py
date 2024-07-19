from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from transformers import pipeline
from pymongo import MongoClient
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import time

# Define schema for incoming data
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("datetime", StringType(), True),
    StructField("userid", StringType(), True),
    StructField("username", StringType(), True),
    StructField("message", StringType(), True)
])

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaSparkHuggingFaceIntegration") \
    .config("spark.mongodb.output.uri", "mongodb://<username>:<password>@localhost:27017/mydatabase.mycollection") \
    .getOrCreate()

# Define Hugging Face pipeline for sentiment analysis
sentiment_analysis_pipeline = pipeline("sentiment-analysis")

# Define UDF to apply Hugging Face sentiment analysis
def sentiment_analysis_udf(message):
    result = sentiment_analysis_pipeline(message)
    return result[0]['label']

# Register the UDF with Spark
sentiment_analysis = udf(sentiment_analysis_udf, StringType())

# Read data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "youtube_chat") \
    .option("startingOffsets", "earliest") \
    .load()

# Deserialize JSON messages
df = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# Apply sentiment analysis UDF to the message column
df_with_sentiment = df.withColumn("sentiment", sentiment_analysis(col("message")))

# Write the DataFrame to MongoDB
df_with_sentiment.writeStream \
    .format("mongo") \
    .option("uri", "mongodb://<username>:<password>@localhost:27017/mydatabase.mycollection") \
    .option("checkpointLocation", "/path/to/checkpoint/dir") \
    .start()

# Aggregate sentiment data for time series analysis
agg_df = df_with_sentiment \
    .withColumn("timestamp", col("timestamp").cast("timestamp")) \
    .groupBy(window(col("timestamp"), "5 seconds"), col("sentiment")) \
    .count() \
    .groupBy("window") \
    .pivot("sentiment") \
    .sum("count") \
    .fillna(0) \
    .withColumn("total", col("positive") + col("negative")) \
    .withColumn("points", col("positive") - col("negative"))

# Function to generate a chart and save it to MongoDB
def save_chart_to_mongodb(df, epoch_id):
    # Convert Spark DataFrame to Pandas DataFrame
    pdf = df.toPandas()

    # Generate the chart using Matplotlib
    plt.figure()
    pdf.plot(x='window', y=['positive', 'negative', 'total', 'points'], kind='line')
    plt.title('Sentiment Analysis Over Time')
    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.legend(loc='upper left')

    # Save the chart as a base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Save the base64 string to MongoDB
    client = MongoClient("mongodb://<username>:<password>@localhost:27017/")
    db = client.mydatabase
    collection = db.time_series_charts
    collection.insert_one({"timestamp": int(time.time()), "chart": img_str})

# Write aggregated data to MongoDB and generate charts
agg_df.writeStream \
    .foreachBatch(save_chart_to_mongodb) \
    .outputMode("update") \
    .option("checkpointLocation", "/path/to/agg/checkpoint/dir") \
    .start() \
    .awaitTermination()

spark.stop()
