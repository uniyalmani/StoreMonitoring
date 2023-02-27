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

def create_consumer(group_id):
    consumer = KafkaConsumer(bootstrap_servers=['kafka:29092'], 
                            auto_offset_reset="earliest",
                            enable_auto_commit=True,
                            group_id= group_id,
                            # key_deserializer=lambda x: loads(x.decode("utf-8")),
                            value_deserializer=lambda x: loads(x.decode("utf-8")))

# Message key: {message.key}
    return consumer

def read_from_topic(topic_name, consumer):
    consumer.subscribe([topic_name])
    print("start consuming")
    for message in consumer:
        message = f""" consuming 
        Message received: {message.value}
        Message partition: {message.partition}
        Message offset: {message.offset}
        """
        print(message)
       
        # csv_head = ["report_id", "up_time_last_week", "down_time_last_week", "up_time_last_day", "down_time_last_day", "up_time_last_hour", "down_time_last_hour"]
        # data = message.value
        

        # # Create a CSV file in memory
        # csv_buffer = io.StringIO()
        # writer = csv.DictWriter(csv_buffer, fieldnames=csv_head)
        # writer.writeheader()
        # for report_id in data:
        #     temp_dct = data[report_id]
        #     row_to_insert = []
        #     for ele in csv_head:
        #         if ele == "report_id":
        #             row_to_insert.append(report_id)
        #             continue
                
        #         row_to_insert.append(temp_dct.get(ele, ""))


        #     writer.writerow(tuple(row_to_insert))
        # csv_data = csv_buffer.getvalue().encode()

        # # Upload the CSV file to S3
        # access_key_id = 'AKIA55RUG4ZW3CVW3YEO'
        # secret_access_key = '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'
        # s3 = boto3.client(
        #     's3',
        #     aws_access_key_id=access_key_id,
        #     aws_secret_access_key=secret_access_key
        # )
        # bucket_name = "csvbucketloop"
        # key = "csvreport" + str(uuid.uuid4()) + ".csv"  # generate a unique key for the file
        # s3.put_object(Bucket=bucket_name, Key=key, Body=csv_data)

        # # Construct URL for the uploaded file
        # file_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
        # print(f"CSV file uploaded to: {file_url}")



env = os.environ

topic_name = env.get('TOPIC_NAME')

consumer1 = create_consumer(group_id="group1")
read_from_topic(topic_name, consumer1)


