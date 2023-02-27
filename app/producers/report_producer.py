from time import sleep
from json import dumps
from kafka import KafkaProducer
import os

producer = KafkaProducer(bootstrap_servers=['kafka:29092'], 
                        value_serializer=lambda x: dumps(x).encode('utf-8'))

# # for i in range(2):
# data = {"number": i}
# print("producing data", data)
# producer.send(topic_name, value=data)
# sleep(2)