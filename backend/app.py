from flask import Flask, jsonify, request
import requests
from mongoengine import *
from datetime import datetime, timedelta, timezone, date, time
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import json
import asyncio
from statsmodels.tsa.arima.model import ARIMA
import pmdarima as pm
import pandas as pd
import talib
import numpy as np 
import pandas as pd
from datetime import datetime
pd.options.mode.chained_assignment = None
import datetime as dt

import pandas as pd
import numpy as np
from datetime import datetime, date, time, timedelta
import nest_asyncio
import json
import asyncio
import aiohttp
import sqlite3

# conn.execute('CREATE TABLE modelresults (prediction REAL, actual_price REAL, percentage_change REAL, tweet_sentiment TEXT, timestamp TEXT)')


from pandas.io.json import json_normalize

from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import swifter
import pickle
nltk.download('stopwords')


nest_asyncio.apply()


app = Flask(__name__)


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)

data_dict = {}

def getdata(date):
    api = f"https://api.polygon.io/v2/aggs/ticker/X:BTCUSD/range/1/minute/{date}/{date}?adjusted=true&sort=asc&limit=1440&apiKey=Ot5XxPIdM4IAsPj6TdlIqHajQFK356JB"
    resp = requests.get(api)
    data = resp.json()
    data_dict[date] = data

async def main(dates, **kwargs):
    for c in dates:
        getdata(c)

def make_ohlcv():
    new_dict = []

    for index,i in enumerate(data_dict):
        if 'results' not in list(data_dict[i].keys()):
            pass
        else:
            new_dict = new_dict + data_dict[i]['results']

    df = pd.DataFrame(new_dict)
    df['timestamp'] = df['t']
    del df['t']
    df['timestamp'] = pd.to_datetime(df['timestamp'],unit = 'ms')
    df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')
    #df['timestamp'] = df['timestamp'].dt.tz_convert('US/Eastern')
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    df = df[['timestamp','o','h','l','c','v']]
    df = df.sort_values(by = 'timestamp')
    df = df.set_index("timestamp")
    df = df.resample('H').mean()
    return df

def preprocess_json(path_):
    with open(path_, encoding="utf8") as f:
        d = json.load(f)
    dataset = json_normalize(d['data'])
    return dataset

def preprocess(dataset):
    dataset = dataset[["created_at", "text", "like_count", "retweet_count", "user_follower_count"]]
    dataset["created_at"] = pd.to_datetime(dataset["created_at"])
    dataset['created_at'] = dataset['created_at'].dt.tz_localize(None)

    dataset["text"] = dataset['text'].str.replace('http\S+|www.\S+', '', case=False)                                              #removing any links
    dataset["text"] = dataset["text"].str.replace('[^A-Za-z\s]+', '')                                                           #removing special chars
    stop = stopwords.words('english')
    dataset["text"] = dataset["text"].swifter.apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

    analyser = SentimentIntensityAnalyzer()
    scores = []
    for i in (range(len(dataset["text"]))):
      score = analyser.polarity_scores(dataset["text"][i])
      scores.append(score)
    dataset[["neg", "nuet", "pos", "compound"]] = pd.DataFrame(scores)
    dataset["like_count"] = pd.to_numeric(dataset.like_count, errors='coerce')
    dataset["retweet_count"] = pd.to_numeric(dataset.retweet_count, errors='coerce')
    if "user_follower_count" in dataset.columns:
        print("Follower count is available in this json!")
        dataset["user_follower_count"] = pd.to_numeric(dataset.user_follower_count, errors='coerce')
        dataset["FinalScore"] = dataset["compound"] * ((dataset["like_count"]) + 1) * ((dataset["retweet_count"]) + 1) * ((dataset["user_follower_count"]) + 1)
    else:
        print("Follower count is not available in this json.")
        dataset["FinalScore"] = dataset["compound"] * ((dataset["like_count"]) + 1) * ((dataset["retweet_count"]) + 1)

    dataset = dataset[["created_at", "text", "FinalScore"]]
    dataset = dataset.rename(columns={'created_at': 'timestamp'})

    return dataset

def make_data_for_model():
    df = pd.read_csv("latest.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["volume"] = df["volume"].astype(float)
    df["close"] = df["close"].astype(float)

    df["close_pct_prev"] = df["close"].pct_change()
    df["EMA2"] = talib.EMA(df["close_pct_prev"], timeperiod=2)
    df["SMA2"] = talib.SMA(df["close_pct_prev"], timeperiod=2)
    df["RSI2"] = talib.RSI(df["close_pct_prev"], timeperiod=2)


    df["open"] = df["open"].pct_change()
    df["high"] = df["high"].pct_change()
    df["low"] = df["low"].pct_change()
    df["FinalScore"] = df["FinalScore"]

    df["EMA2_open"] = talib.EMA(df["open"], timeperiod=2)
    df["EMA2_high"] = talib.EMA(df["high"], timeperiod=2)
    df["EMA2_low"] = talib.EMA(df["low"], timeperiod=2)

    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.dropna()
    return df

def predict_future(df_path, model_path):
    exg_features = ["EMA2_open", "EMA2_low", "EMA2", "SMA2", "FinalScore"]
    df = pd.read_csv(df_path)
    with open(model_path , 'rb') as f:
        model = pickle.load(f)
    forecast = model.predict(n_periods=len(df), exogenous = df[exg_features])
    df["Forecast_ARIMAX"] = forecast
    metrics_df = df[["timestamp", "Forecast_ARIMAX"]]
    return metrics_df

def connect_to_twitter():
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAIqqWwEAAAAAfFTNW92Qxfm0fiO817xjFUFZh3k%3D8dmSrI7SH9rCDRCvSlcZ7lMWxUHr1AAmsBjSKTmGf0b8lG7Oar"
    return {"Authorization": "Bearer {}".format(bearer_token)}

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

def get_user_obj(users, uid):
    for user in users:
        if user["id"] == uid:
            return {"id": user["id"], "follower_count": user["public_metrics"]["followers_count"]}


def fetch_recent_tweets():
    headers = connect_to_twitter()
    all_data = {"data": []}
    next_token = {}
    error_occured = False
    userids = []
    userobjcs = {}
    while(next_token != None):
        ii = 0
        for ii in tqdm(range(300)):
            try:
                response = make_request(headers, next_token)
                if "next_token" in response["meta"].keys():
                    next_token = response["meta"]["next_token"]
                    print(response["meta"]["next_token"])
                else:
                    print("fetching done")
                    next_token = None
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
                print("Error Occured")
                print("last used", next_token)
                print(e)
                # with open('recent.json', 'w', encoding='utf-8') as f:
                #     all_data["next_token"] = next_token
                #     json.dump(all_data, f, ensure_ascii=False, indent=4)
                error_occured = True
            if error_occured or next_token == None:
                print("ended", next_token)
                break
        if error_occured or next_token == None:
            break
        time.sleep(360)
    print("Total retrieved final: ", len(all_data["data"]))
        
    with open('recent.json', 'w', encoding='utf-8') as f:
        all_data["next_token"] = next_token
        json.dump(all_data, f, ensure_ascii=False, indent=4)



@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/get/all')
def getall():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    res = curr.execute("SELECT * FROM modelresults")
    r = res.fetchall()
    curr.close()
    conn.commit()
    conn.close()
    final = []
    print(r)
    for i in range(len(r)):
        if i < len(r) - 1:
            final.append({
                "prediction": r[i][0],
                "actual_price": r[i][1],
                "percentage_change": r[i][2],
                "sentiment": r[i][3],
                "timestamp": r[i][4]
            })
    return jsonify({"result": final})

@app.route('/get/tmp')
def gettmp():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    res = curr.execute("SELECT * FROM modelresults")
    r = res.fetchall()
    curr.close()
    conn.commit()
    conn.close()
    final = []
    print(r)
    for i in range(len(r)):
        final.append({
            "prediction": r[i][0],
            "actual_price": r[i][1],
            "percentage_change": r[i][2],
            "sentiment": r[i][3],
            "timestamp": r[i][4]
        })
    return jsonify({"result": final})


@app.route('/get/search')
def getsearch():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    res = curr.execute("UPDATE modelresults SET actual_price=? WHERE timestamp=(SELECT timestamp FROM modelresults ORDER BY timestamp DESC LIMIT 1)", (10,))
    # r = res.fetchall()
    curr.close()
    conn.commit()
    conn.close()
    final = []
    # print(r)
    # for i in range(len(r)):
    #     final.append({
    #         "prediction": r[i][0],
    #         "actual_price": r[i][1],
    #         "percentage_change": r[i][2],
    #         "sentiment": r[i][3],
    #         "timestamp": r[i][4]
    #     })
    # return jsonify({"result": final})
    return 'a'

@app.route('/upd/tmp')
def updtmp():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor() #29715.41
    curr.execute("UPDATE modelresults SET actual_price=? WHERE prediction=?", (29569.81,29449.367933804544))
    curr.close()
    conn.commit()
    conn.close()
    return jsonify({})


@app.route('/del/tmp')
def deltimp():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor() #29715.41
    curr.execute("DELETE FROM modelresults WHERE tweet_sentiment=?", ("116661.6759555",))
    curr.close()
    conn.commit()
    conn.close()
    return jsonify({})

@app.route('/get/latest')
def getlatest():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    res = curr.execute("SELECT * FROM modelresults ORDER BY timestamp DESC LIMIT 1")
    r = res.fetchall()
    curr.close()
    conn.commit()
    conn.close()
    final = []
    print(r)
    for i in range(len(r)):
        final.append({
            "prediction": r[i][0],
            "actual_price": r[i][1],
            "percentage_change": r[i][2],
            "sentiment": r[i][3],
            "timestamp": r[i][4]
        })
    return jsonify({"result": final})



@app.route('/predict', methods=['GET'])
async def predict_btc():
    # getting start and end time for polygon data fetching
    polygon_endtime = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
    polygon_starttime = polygon_endtime - timedelta(days = 1, hours=0, minutes=60)
    print("polygon end", polygon_endtime)
    print("polygon start", polygon_starttime)
    dates = []
    # fetching polygon data
    # 1- fetch ohlcv from start to end
    for i in daterange(pd.to_datetime(polygon_starttime), pd.to_datetime(polygon_endtime)):
        dates.append(i.date().strftime("%Y-%m-%d"))
    print("before")
    await main(dates)
    print("after")

    df = make_ohlcv()
    df = df.rename({"o" : "open", "h" : "high", "l" : "low", "c" : "close", "v" : "volume"}, axis = 1)
    print(df)
    close_price = df["close"].values[-1]
    # fetch tweets
    fetch_recent_tweets()
    dff = preprocess_json("recent.json")
    new_df = preprocess(dff)
    print("after preprocessing tweets")
    print(new_df)

    tweet_df = new_df[["timestamp", "FinalScore"]]
    tweet_df["timestamp"] = pd.to_datetime(tweet_df["timestamp"])
    tweet_df = tweet_df.sort_values(by = "timestamp")
    tweet_df = tweet_df.reset_index(drop = True)
    tweet_df = tweet_df.set_index("timestamp")
    tweet_df = tweet_df.resample('60Min').mean()
    last_score = tweet_df["FinalScore"].values[-1]

    FinalScore = [0] * (len(df) -1)
    FinalScore.append(last_score)

    df["FinalScore"] = FinalScore

    df.to_csv("latest.csv")

    df_fin = make_data_for_model()

    df_fin.to_csv("altuu.csv")

    fin_df = predict_future("altuu.csv", "ARIMAX.pkl")
    print("Final Pickle: ", fin_df)
    perc_change = fin_df["Forecast_ARIMAX"].values[-1]
    print("percentage change predicted:"+str(perc_change))
    timestmp = polygon_endtime + timedelta(hours=0, minutes=60)
    timestmp = timestmp + timedelta(hours=5)
    # polygon_endtime = polygon_endtime + timedelta(hours=5)
    print(timestmp)
    predicted_price = close_price + (close_price*perc_change)
    print(close_price)
    print(predicted_price)
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute("UPDATE modelresults SET actual_price=? WHERE timestamp=(SELECT timestamp FROM modelresults ORDER BY timestamp DESC LIMIT 1)", (close_price,))

    # conn.execute('UPDATE modelresults SET actual_price=? WHERE timestamp=?',(close_price, polygon_endtime, ))
    conn.execute('INSERT INTO modelresults (prediction, actual_price, percentage_change, tweet_sentiment, timestamp) VALUES (?,?,?,?,?)', (predicted_price, 0, perc_change, last_score, timestmp))
    conn.commit()
    conn.close()

    # 2- preprocessing
    # 3- predict
    # 4- finalize
    return data_dict