import os
from fastapi import FastAPI, Response, status
from typing import Dict, List, Optional
from sqlmodel import Field, SQLModel, select
from app.utilities.dependencies import get_session
from app.models.database_models import StoreStatus, StoreSchedule, StoreTimezone
from app.utilities.helpers import store_wise_parser, store_wise_opening_time, find_up_and_down_time, get_start_end_of_date
import datetime
from collections import defaultdict


class Report:
    def __init__(self):
        self.session = next(get_session())

    def get_prev_week_data(self, given_time_str):
        try:
            # Example time in UTC timezone
            given_time = datetime.datetime.strptime(given_time_str, '%Y-%m-%d %H:%M:%S.%f %Z').replace(tzinfo=datetime.timezone.utc)

            # Determine the start and end dates of the week that includes the given time
            week_start = given_time - datetime.timedelta(days=given_time.weekday())
            week_end = week_start + datetime.timedelta(days=6)

            # Determine the start and end dates of the week before the current week
            prev_week_end = week_start - datetime.timedelta(days=1)
            prev_week_start = prev_week_end - datetime.timedelta(days=6)
            
            # query = select(StoreTimezone)
            # time_zone = self.session.exec(query).all()

            query = select(StoreStatus).where(StoreStatus.timestamp_utc <= prev_week_end, StoreStatus.timestamp_utc >= prev_week_start)
            
            last_week_status = self.session.exec(query).all()
           
            data  = store_wise_parser(last_week_status)
            store_wise_data, store_wise_status_count = data["store_wise_data"], data["store_wise_status_count"]
            total_time_open_store = self.get_total_opening_time_store(0, 6)
            
            final_week_data = defaultdict()
            
            for store_id in store_wise_status_count:
                status_count_dict = store_wise_status_count[store_id]
                active_count, inactive_count = status_count_dict.get("active", 0), status_count_dict.get("inactive", 0)
                total_schedule_opening = total_time_open_store[store_id]
                up_time_last_week, down_time_last_week = find_up_and_down_time(active_count, inactive_count, total_schedule_opening)
                final_week_data[store_id] = {"up_time_last_week": up_time_last_week, "down_time_last_week":down_time_last_week}

            return final_week_data

        except Exception as e:
            print(e)
            return {
                "error": e

            }
    def get_total_opening_time_store(self, start_day, end_day):
        
        query = select(StoreSchedule).where(start_day <= StoreSchedule.dayOfWeek, StoreSchedule.dayOfWeek  <= end_day)
            
        store_schedule_res = self.session.exec(query).all()
        
        data = store_wise_opening_time(store_schedule_res)
        
        return data
    
    def get_prev_data(self, given_time_str, time_delta):

        start_datetime, end_datetime = get_start_end_of_date(given_time_str, time_delta)
        weekday = start_datetime.weekday()

        query = select(StoreStatus).where(StoreStatus.timestamp_utc <= end_datetime, StoreStatus.timestamp_utc >= start_datetime)
            
        last_day_status = self.session.exec(query).all()

        data  = store_wise_parser(last_day_status)
        store_wise_data, store_wise_status_count = data["store_wise_data"], data["store_wise_status_count"]
        
        total_time_open_store = self.get_total_opening_time_store(weekday, weekday)


        final_day_data = defaultdict()
        for store_id in store_wise_status_count:
                status_count_dict = store_wise_status_count[store_id]
                active_count, inactive_count = status_count_dict.get("active", 0), status_count_dict.get("inactive", 0)
                total_schedule_opening = total_time_open_store[store_id]
                if time_delta != 0:
                    up_time_last_day, down_time_last_day = find_up_and_down_time(active_count, inactive_count, total_schedule_opening)
                    final_day_data[store_id] = {"up_time_last_day": up_time_last_day, "down_time_last_day":down_time_last_day}
                else:
                    up_time_last_hour, down_time_last_hour = find_up_and_down_time(active_count, inactive_count, total_schedule_opening, req_range=3600)
                    final_day_data[store_id] = {"up_time_last_hour": up_time_last_hour, "down_time_last_hour":down_time_last_hour}


        return final_day_data

    def get_all_store(self):
        query = select(StoreTimezone.store_id)
            
        store_list = self.session.exec(query).all()
        print(store_list)
        return store_list