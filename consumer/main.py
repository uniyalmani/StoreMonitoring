# from consumer_app.consumer import  create_topic
# from consumer import create_consumer, read_from_topic
from time import sleep
from json import dumps, loads
from kafka import KafkaConsumer
import os
import boto3
import csv
import io
import uuid





# env = os.environ

# topic_name = env.get('TOPIC_NAME')

# consumer1 = create_consumer(group_id="group1")
# read_from_topic(topic_name, consumer1)


