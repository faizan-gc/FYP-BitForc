import pandas as pd
import requests
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
    print(type(yesterday))
    print(type(enddate))
    yesterday = yesterday.split('+')[0]
    enddate = enddate.split('+')[0]
    enddate += ".000Z"
    yesterday += ".000Z"
    print(yesterday)
    print(enddate)
    url = "https://api.twitter.com/2/tweets/search/all"
    query_params = {'query': 'bitcoin lang:en',
    'max_results': 500,
    "start_time": yesterday,
    "end_time": enddate,
    "expansions": "author_id",
    'tweet.fields': 'id,text,created_at,public_metrics',
    'user.fields': 'id,public_metrics',
    'next_token': n}
    return requests.request("GET", url, params=query_params, headers=headers).json()

all_data = {"data": []}
next_token = {}
de = False

# rr = make_request(headers, "b26v89c19zqg8o3fpe7892z2qm8s46tnrhwhxcqt89t31")
# print(rr)
# arr = []
userids = []
userobjcs = {}

def get_user_obj(users, uid):
  for user in users:
    if user["id"] == uid:
      return {"id": user["id"], "follower_count": user["public_metrics"]["followers_count"]}

# for i in range(len(rr["data"])):
#   if rr["data"][i]["author_id"] not in userids:
#     uobj = get_user_obj(rr["includes"]["users"], rr["data"][i]["author_id"])
#     userobjcs[rr["data"][i]["author_id"]] = uobj
#     userids.append(rr["data"][i]["author_id"])
#   d = {
#     "text": rr["data"][i]["text"],
#     "id": rr["data"][i]["id"],
#     "created_at": rr["data"][i]["created_at"],
#     "author_id": rr["data"][i]["author_id"],
#     "retweet_count": rr["data"][i]["public_metrics"]["retweet_count"],
#     "like_count": rr["data"][i]["public_metrics"]["like_count"],
#     "user_details": userobjcs[rr["data"][i]["author_id"]]
#   }
#   arr.append(d)
# all_data["data"].extend(arr)
# print(all_data)
# print(len(all_data["data"]))

while(next_token != None):
  ii = 0
  for ii in tqdm(range(300)):
    try:
      response = make_request(headers, next_token)
      next_token = response["meta"]["next_token"]
      print(response["meta"]["next_token"])
      arr = []
      for i in range(len(response["data"])):
        if response["data"][i]["author_id"] not in userids:
          uobj = get_user_obj(response["includes"]["users"], response["data"][i]["author_id"])
          userobjcs[response["data"][i]["author_id"]] = uobj
          userids.append(response["data"][i]["author_id"])
        d = {
          "text": response["data"][i]["text"],
          "id": response["data"][i]["id"],
          "created_at": response["data"][i]["created_at"],
          "author_id": response["data"][i]["author_id"],
          "retweet_count": response["data"][i]["public_metrics"]["retweet_count"],
          "like_count": response["data"][i]["public_metrics"]["like_count"],
          "user_follower_count": userobjcs[response["data"][i]["author_id"]]["follower_count"]
        }
        arr.append(d)
      all_data["data"].extend(arr)
    except Exception as e:
      print("err", e)
      print("last used", next_token)
      print("errorrr")
      print(len(all_data["data"]))
      with open('recent.json', 'w', encoding='utf-8') as f:
        all_data["next_token"] = next_token
        json.dump(all_data, f, ensure_ascii=False, indent=4)
      de = True
    if de or next_token == None:
      print("ended", next_token)
      break
  if de:
    break
  else:
    with open('recent.json', 'w', encoding='utf-8') as f:
      all_data["next_token"] = next_token
      json.dump(all_data, f, ensure_ascii=False, indent=4)
    print("One round complete", len(all_data["data"]))
    time.sleep(360)

if not de:
  with open('recent.json', 'w', encoding='utf-8') as f:
    all_data["next_token"] = next_token
    json.dump(all_data, f, ensure_ascii=False, indent=4)
print(len(all_data["data"]))

