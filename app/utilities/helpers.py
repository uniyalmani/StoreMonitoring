from collections import defaultdict
from datetime import datetime, timedelta, time, timezone



def formate_num(number):
    return '{:02}'.format(number)


def add_times(time1_str: str = "00:00:00", time2_str: str = "00:00:00") -> str:
    """Add two time strings in the format 'HH:MM:SS'."""
    time1 = list( map(int, time1_str.split(":")))
    time2 = list( map(int, time2_str.split(":")))
    seconds, minutes, hours, days =0, 0, 0, 0
    carry = 0
    seconds, carry = (time2[2] + time1[2] + carry)%60, (time2[2] + time1[2])//60
    minutes, carry = (time2[1] + time1[1] + carry)%60, (time2[1] + time1[1])//60
    hours = time2[0] + time1[0] + carry

    return f"{hours}:{minutes}:{seconds}"

def time_diff(time_str1: str, time_str2: str) -> datetime:
    """Calculate the time difference between two time strings in the format 'HH:MM:SS'."""

    time_format = "%H:%M:%S"
    time1 = datetime.strptime(time_str1, time_format).time()
    time2 = datetime.strptime(time_str2, time_format).time()
    today_date = datetime.now().date()

    if time2 < time1:
        # add a day to time2 if it's earlier than time1
        time2 = (datetime.combine(today_date, time2) + timedelta(days=1)).time()
    time_diff = datetime.combine(today_date, time2) - datetime.combine(today_date, time1)

    return f"{time_diff.seconds // 3600}:{(time_diff.seconds // 60) % 60}:{time_diff.seconds % 60}"

def store_wise_parser(data: list[object]):
    dct = defaultdict(list)
    store_wise_status_count = defaultdict(dict)
    for d in data:
        dct[d.store_id].append(d) 
        store_wise_status_count[d.store_id][d.status.name] = store_wise_status_count[d.store_id].get(d.status.name, 0) + 1
    
    return {"store_wise_data":dct,  "store_wise_status_count": store_wise_status_count}


def  store_wise_opening_time(data: list[object]):
    time_format = "%H:%M:%S"
    dct = defaultdict(lambda:"00:00:00")
    
    for d in data:
        start_time_str = d.start_time_local
        end_time_str = d.end_time_local
        open_time = time_diff(start_time_str, end_time_str)
        dct[d.store_id] = add_times(dct[d.store_id],open_time)
    
    return dct


def change_seconds_to_h_m_s_formate(total_seconds):
    
    minutes, hours, days =0, 0, 0
    carry = 0
    seconds = (total_seconds)%60
    total_seconds = (total_seconds - seconds)
    total_minutes  = total_seconds//60
    minutes =total_minutes%60
    total_minutes = total_minutes - minutes
    hours = total_minutes//60
    seconds, minutes, hours = formate_num(seconds), formate_num(minutes), formate_num(hours)
    return f"{hours}:{minutes}:{seconds}" 


def find_up_and_down_time(active_count: int, inactive_count: int, total_schedule_opening: int, req_range: int = 0):

    hours, minutes, seconds = list(map(int,total_schedule_opening.split(":")))
    total_opening_in_seconds = 3600*hours + minutes*60 + seconds
    if total_opening_in_seconds == 0:
         return "00:00:00", "00:00:00"
    
    inactive_seconds = inactive_count*((total_opening_in_seconds)//(inactive_count + active_count))
    active_seconds = total_opening_in_seconds - inactive_seconds
    
    if req_range:
        inactive_seconds = (req_range*inactive_seconds)//total_opening_in_seconds
        active_seconds =  (req_range*active_seconds)//total_opening_in_seconds
    

    uptime = change_seconds_to_h_m_s_formate(active_seconds)
    downtime = change_seconds_to_h_m_s_formate(inactive_seconds)

    return uptime, downtime


def get_start_end_of_date(given_time_str, time_delta: int):
    given_time = datetime.strptime(given_time_str, '%Y-%m-%d %H:%M:%S.%f %Z').replace(tzinfo=timezone.utc)
    yesterday = given_time - timedelta(days=time_delta)

    # get start and end datetime of yesterday
    start_datetime = datetime.combine(yesterday, time.min)
    end_datetime = datetime.combine(yesterday, time.max)

    return start_datetime, end_datetime


