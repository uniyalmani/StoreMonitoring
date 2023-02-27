from time import sleep
from json import dumps, loads
from kafka import KafkaConsumer
import os
import boto3
import csv
import io
import uuid
from collections import defaultdict

env = os.environ

access_key_id = env.get("S3_ACCESS_KEY_ID")
aws_secret_access_key = env.get("S3_AWS_SECRET_ACCESS_KEY")
bucket_name = env.get("BUCKET_NAME")
topic_name = env.get("TOPIC_NAME")
global_dict_tracker = defaultdict(list) 
csv_head = ["store_id", "up_time_last_week", "down_time_last_week", "up_time_last_day", "down_time_last_day", "up_time_last_hour", "down_time_last_hour"]

def create_csv(data, csv_head, dict_id):
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(csv_head)
    # writer = csv.DictWriter(csv_buffer, fieldnames=csv_head)
    # writer.writeheader()
    for d in data:
        print(d, "llll")
        writer.writerow(d)
    csv_buffer_obj = csv_buffer.getvalue().encode()

    return csv_buffer_obj

def upload_csv_to_s3(bucket_name ,dict_id, csv_buffer_obj):

    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    key = "csvreport" + dict_id + ".csv"  # generate a unique key for the file
    s3.put_object(Bucket=bucket_name, Key=key, Body=csv_buffer_obj)

    # Construct URL for the uploaded file
    file_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
    
    return {"url": file_url, "message": "uploaded"}



def create_consumer(topic_name, group_id):

    consumer = KafkaConsumer(bootstrap_servers=['kafka:29092'], 
                            auto_offset_reset="earliest",
                            enable_auto_commit=True,
                            group_id= "group1",
                            # key_deserializer=lambda x: loads(x.decode("utf-8")),
                            value_deserializer=lambda x: loads(x.decode("utf-8")))


    consumer.subscribe([topic_name])

    return consumer



def consume_messages(consumer, csv_head):
    
    i = 1
    
    
    for message in consumer:
        # print(type(message), dir(message),type(message.value))
        # Get chunk and dict_id from message
        chunk = message.value
        dict_id = chunk['dict_id']
        temp = []
        for ele in csv_head:
            temp.append(chunk[ele])
        global_dict_tracker[dict_id].append(temp)
            

        if chunk["current_chuck_number"] == chunk["total_chucks"]:
            return dict_id
            upload_csv_to_s3(global_dict_tracker[dict_id], csv_head, dict_id)


consumer = create_consumer(topic_name, "group1")

dict_id = consume_messages(consumer, csv_head)
data = global_dict_tracker[dict_id]
csv_buffer_obj = create_csv(data , csv_head, dict_id)
upload_csv_to_s3(bucket_name, dict_id, csv_buffer_obj)
del global_dict_tracker[dict_id]