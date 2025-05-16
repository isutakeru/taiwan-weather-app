import os

import os
from datetime import datetime

def save_to_csv(df, city, folder="data"):
    """
    DataFrame を CSV に保存する（ファイル名に日付付き）

    例: data/20240517_臺南市_weather.csv
    """
    os.makedirs(folder, exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{folder}/{date_str}_{city}_weather.csv"

    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"✅ Saved to {filename}")
