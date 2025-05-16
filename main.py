from dotenv import load_dotenv
import os
import schedule
import time

from src.fetch_weather import fetch_weather_data
from src.transform_weather import transform_weather_data
from src.save_csv import save_to_csv
from src.save_excel import save_all_to_excel  # ✅ 追加

load_dotenv()
API_KEY = os.getenv("CWB_API_KEY")

cities = ["臺北市", "高雄市", "臺南市", "臺東縣"]

def run_weather_etl():
    print("🌤️ 天氣データ取得開始")
    all_data = {}

    for city in cities:
        print(f"📡 取得中: {city}")
        data = fetch_weather_data(API_KEY, city)

        if not data or not data["records"]["location"]:
            print(f"⚠️ {city} の天気データが見つかりません。スキップします。")
            continue

        try:
            df = transform_weather_data(data)
            print(f"✅ {city} のデータを DataFrame に変換成功")
            save_to_csv(df, city)
            all_data[city] = df  # Excel用に保存
        except Exception as e:
            print(f"❌ {city} のデータ変換に失敗: {e}")

    if all_data:
        save_all_to_excel(all_data)
        print("✅ Excelファイル保存完了")
    else:
        print("⚠️ 保存できるデータがありません")


# ✅ 毎日9時に実行スケジュールを設定
schedule.every().day.at("23:53").do(run_weather_etl)

print("⏳ スケジュールを開始します... Ctrl+Cで停止")

while True:
    schedule.run_pending()
    time.sleep(60)
