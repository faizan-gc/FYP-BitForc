import pandas as pd
import requests
import os
import json
import time
from tqdm import tqdm
from datetime import datetime, timedelta, timezone

def connect_to_twitter():
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAIqqWwEAAAAAfFTNW92Qxfm0fiO817xjFUFZh3k%3D8dmSrI7SH9rCDRCvSlcZ7lMWxUHr1AAmsBjSKTmGf0b8lG7Oar"
    return {"Authorization": "Bearer {}".format(bearer_token)}
headers = connect_to_twitter()

def make_request(headers, n):

    enddate = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
    yesterday = enddate - timedelta(hours=0, minutes=120)
    enddate = enddate.isoformat()
    yesterday = yesterday.isoformat()
    yesterday = yesterday.split('+')[0]
    enddate = enddate.split('+')[0]
    enddate += ".000Z"
    yesterday += ".000Z"
    url = "https://api.twitter.com/2/tweets/counts/all"
    query_params = {'query': 'bitcoin lang:en',
    "start_time": yesterday,
    "end_time": enddate}
    return requests.request("GET", url, params=query_params, headers=headers).json()
all_data = {"data": []}
next_token = {}
de = False

response = make_request(headers, next_token)
# next_token = response["meta"]["next_token"]
print(response)

