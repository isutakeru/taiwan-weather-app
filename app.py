import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

from src.fetch_weather import fetch_weather_data
from src.transform_weather import transform_weather_data
from src.save_excel import save_all_to_excel
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

load_dotenv()
API_KEY = os.getenv("CWB_API_KEY")

st.set_page_config(page_title="台灣天氣查詢系統", layout="centered")

st.title("🌤️ 台灣天氣查詢系統")
st.markdown("請選擇想查詢的城市，點選按鈕以取得最新 36 小時天氣預報。")

city = st.selectbox("選擇城市", ["臺北市", "高雄市", "臺南市", "臺東縣"])

if st.button("取得天氣"):
    data = fetch_weather_data(API_KEY, city)

    if not data or not data["records"]["location"]:
        st.warning("⚠️ 無法取得天氣資料，請稍後再試。")
    else:
        df = transform_weather_data(data)
        st.success(f"✅ {city} 的天氣資料取得成功！")

        st.dataframe(df)

        # 👉 折線圖：最低與最高溫度趨勢
        fig_temp, ax_temp = plt.subplots()
        ax_temp.plot(df["Start Time"], df["Min Temp"], marker='o', label='最低溫度', color='blue')
        ax_temp.plot(df["Start Time"], df["Max Temp"], marker='o', label='最高溫度', color='red')
        ax_temp.set_xlabel("時間")
        ax_temp.set_ylabel("攝氏溫度")
        ax_temp.set_title(f"{city} 未來36小時氣溫趨勢")
        ax_temp.legend()
        ax_temp.grid(True)
        st.pyplot(fig_temp)

        # 👉 長條圖：降雨機率
        fig_rain, ax_rain = plt.subplots()
        ax_rain.bar(df["Start Time"], df["Rain (%)"].astype(int), color='skyblue')
        ax_rain.set_xlabel("時間")
        ax_rain.set_ylabel("降雨機率 (%)")
        ax_rain.set_title(f"{city} 未來36小時降雨機率")
        ax_rain.grid(axis='y')
        st.pyplot(fig_rain)


        csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 下載 CSV 檔案", csv, file_name=f"{city}_天氣預報.csv")

        date_str = datetime.now().strftime("%Y%m%d")
        excel_path = f"data/{date_str}_{city}_天氣預報.xlsx"
        df.to_excel(excel_path, index=False)
        with open(excel_path, "rb") as f:
            st.download_button("📥 下載 Excel 檔案", f, file_name=f"{city}_天氣預報.xlsx")
