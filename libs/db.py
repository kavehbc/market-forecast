import json
import pandas as pd
import os

local_db_path = "db/popular.json"
db_folder = "/tmp"
db_path = "/tmp/popular.json"


def get_file_path(mode="open"):
    if os.path.exists(db_folder):
        if os.path.exists(db_path) or mode == "save":
            file_path = db_path
        elif mode == "open":
            file_path = local_db_path
    else:
        file_path = local_db_path
    return file_path


def read_db():
    file_to_open = get_file_path(mode="open")
    with open(file_to_open) as f:
        json_data = json.load(f)
        return json_data


def save_db(json_data):
    file_to_save = get_file_path(mode="save")
    with open(file_to_save, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    # save sorted data
    sort_json()


def sort_json():
    file_to_open = get_file_path(mode="open")
    file_to_save = get_file_path(mode="save")
    unsorted = pd.read_json(file_to_open)
    (unsorted.sort_values("count", ascending=False)).to_json(file_to_save, orient='records')


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
    file_to_open = get_file_path(mode="open")
    df_tickers = pd.read_json(file_to_open)
    return df_tickers


def reset_tmp_db():
    if os.path.exists(db_path):
        os.remove(db_path)
        return True
    return False
