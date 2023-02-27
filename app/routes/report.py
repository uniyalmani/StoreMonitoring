from pydantic import BaseModel, validator
from fastapi import APIRouter, Depends
from app.services.report import Report
from app.producers.report_producer import producer
from collections import defaultdict
from app.utilities.helpers import formate_num
import boto3
import uuid
import os



router = APIRouter()

env = os.environ

topic_name = env.get("TOPIC_NAME")
access_key_id = env.get("S3_ACCESS_KEY_ID")
aws_secret_access_key = env.get("S3_AWS_SECRET_ACCESS_KEY")
bucket_name = env.get("BUCKET_NAME")



@router.get('/trigger_report',
        tags=["Common Routes"],
        description="**genrate report**")
def trigger_report():
    report_info = Report()
    given_date = "2023-01-30 12:09:39.388884 UTC"

    last_week_data = report_info.get_prev_week_data(given_date)

    last_day_data = report_info.get_prev_data( given_date, 1)

    last_hour_data = report_info.get_prev_data( given_date, 0)

    store_list = set(report_info.get_all_store())

    final_data = {}
    chunk_size = 1
    total_chucks = len(store_list)
    dict_id = str(uuid.uuid4())
    current_chuck_number = 1

    for store_id in store_list:

        final_data[store_id] = {"up_time_last_week": "00:00:00", "down_time_last_week": "00:00:00","up_time_last_day": "00:00:00", "down_time_last_day": "00:00:00","up_time_last_hour": "00:00:00", "down_time_last_hour": "00:00:00"}
        final_data[store_id]["store_id"] = store_id

        if store_id in last_week_data:
            final_data[store_id]["up_time_last_week"] = last_week_data[store_id]["up_time_last_week"]
            final_data[store_id]["down_time_last_week"] = last_week_data[store_id]["down_time_last_week"]
        if store_id in last_day_data:
            final_data[store_id]["up_time_last_day"] = last_day_data[store_id]["up_time_last_day"]
            final_data[store_id]["down_time_last_day"] = last_day_data[store_id]["down_time_last_day"]
        if store_id in last_hour_data:
            final_data[store_id]["up_time_last_hour"] = last_hour_data[store_id]["up_time_last_hour"]
            final_data[store_id]["down_time_last_hour"] = last_hour_data[store_id]["down_time_last_hour"]

        chunk = final_data[store_id]
        
        chunk["total_chucks"] = total_chucks
        chunk["dict_id"] = dict_id
        chunk["current_chuck_number"] =  current_chuck_number

        producer.send(topic_name, chunk)
        current_chuck_number += 1

        producer.flush()
    producer.close()
        

    return {
        "message" : "start building",
        "report_id": dict_id
    }

@router.get('/get_report',
        tags=["Common Routes"],
        description="**genrate report**")
def get_report(report_id):

    key = "csvreport" + report_id + ".csv"
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    try:
       
        response = s3.head_object(Bucket="csvbucketloop", Key=key)
        url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
        return {
            "status": "Complete",
            "download_url": url,
            "report_schema":("store_id(str)",
                              "up_time_last_week(HH:MM:SS)", "down_time_last_week(HH:MM:SS)", "up_time_last_day(HH:MM:SS)",
                                "down_time_last_day(HH:MM:SS)", "up_time_last_hour(HH:MM:SS)", "down_time_last_hour(HH:MM:SS)")
        }
    except Exception as e:
        return {
            "status": "Running"
        }
