import os
from datetime import datetime
import pandas as pd

def save_all_to_excel(data_dict, folder="data"):
    """
    複数都市の DataFrame を Excel にシート分けで保存する

    Parameters:
        data_dict (dict): {"都市名": DataFrame, ...}
        folder (str): 保存フォルダ
    """
    os.makedirs(folder, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{folder}/{date_str}_weather_summary.xlsx"

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        for city, df in data_dict.items():
            df.to_excel(writer, sheet_name=city[:31], index=False)  # シート名は最大31文字

    print(f"✅ Excelファイル保存完了: {filename}")
