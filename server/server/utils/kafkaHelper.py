from kafka import KafkaProducer, KafkaConsumer
import json
import datetime as dt

def initProducer():
    print('Initializing Kafka producer at {}'.format(dt.datetime.utcnow()))
    producer = KafkaProducer(
      bootstrap_servers='localhost:9092',
      value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    return producer

def initConsumer(topic, timeout=1000):
    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', group_id=None,
        auto_offset_reset='earliest', enable_auto_commit=False, consumer_timeout_ms=timeout,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m.strip() else None)
    return consumer

def produceData(topic_name, producer, data):
    producer.send(topic=topic_name, value=data)
    producer.flush()
    print('Data sent at {}'.format(dt.datetime.utcnow()))
    
def consumeData(consumer):
    rec_list = []
    for rec in consumer:
        r = rec.value
        rec_list.append(r)
    
    return rec_list