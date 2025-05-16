# fetch_weather.py
import requests
from dotenv import load_dotenv
import os

def fetch_weather_data(api_key, location="臺南市"):
    """
    中央氣象局の36時間天氣預報APIから、指定した都市の天気情報を取得する

    Parameters:
        api_key (str): CWB OpenData API key
        location (str): 取得する都市名（例：臺南市、臺北市）

    Returns:
        dict: APIから返されたJSONデータ
    """
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"

    params = {
        "Authorization": api_key,
        "locationName": location
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # エラーがあれば例外を出す
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
        return None
