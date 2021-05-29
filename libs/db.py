import json
import pandas as pd

db_path = "db/popular.json"


def read_db():
    with open(db_path) as f:
        json_data = json.load(f)
        return json_data


def save_db(json_data):
    # json_data = json.dumps(json_data) # , indent=4
    with open(db_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    # save sorted data
    sort_json()


def sort_json():
    unsorted = pd.read_json(db_path)
    (unsorted.sort_values("count", ascending=False)).to_json(db_path, orient='records')


def update_db(ticker_name):
    update_flag = False
    json_data = read_db()
    for ticker in json_data:
        if str(ticker["ticker"]) == str(ticker_name):
            ticker["count"] += 1
            update_flag = True

    # ticker did not exist in the db
    if not update_flag:
        json_data.append({"ticker": ticker_name, "count": 1})
        update_flag = True

    if update_flag:
        save_db(json_data)


def get_top_tickers(n=100):
    counter = 0
    tickers = []
    json_data = read_db()
    for ticker in json_data:
        if counter >= n:
            break
        tickers.append(ticker["ticker"])
        counter += 1
    return tickers


def tickers_to_df():
    df_tickers = pd.read_json(db_path)
    return df_tickers
