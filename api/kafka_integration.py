import os

from confluent_kafka import Producer

conf = {
    'bootstrap.servers': os.getenv('KAFKA', 'localhost:9092'),
}

producer = Producer(conf)


def send_kafka_message(topic, key, value):
    topic = topic.replace(' ', '_')
    producer.produce(topic, key=key, value=value)
    producer.poll(0)
    producer.flush()
