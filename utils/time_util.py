import time
from datetime import datetime


def get_current_timestamp():
    current_timestamp = int(time.time())
    return current_timestamp


def timestamp_to_datetime(timestamp):
    """ 将时间戳转化成datetime时间类型的数据 """
    return datetime.fromtimestamp(timestamp)
