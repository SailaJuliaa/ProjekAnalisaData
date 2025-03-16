import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")
st.title(" Dashboard Penyewaan Sepeda")

@st.cache_data
def load_data():
    df = pd.read_csv("D:\\DBS_coding\\Bike_dashboard\\all_data.csv")  
    df['dteday'] = pd.to_datetime(df['dteday']) 
    return df

df = load_data()

st.sidebar.header(" Pilih Tanggal")
selected_date = st.sidebar.date_input("Pilih tanggal:", df['dteday'].min())

daily_data = df[df['dteday'] == pd.to_datetime(selected_date)]

st.subheader(f" Data Penyewaan Sepeda pada {selected_date}")
if not daily_data.empty:
    col1, col2 = st.columns(2)
    
    # Total penyewaan
    total_rentals = daily_data['cnt'].values[0]
    col1.metric("Total Penyewaan", total_rentals)
    
    # Cuaca lebih detail
    weather_map = {1: "Cerah", 2: "Berkabut", 3: "Hujan Ringan", 4: "Hujan Lebat"}
    weather = weather_map.get(daily_data['weathersit'].values[0], "Tidak Diketahui")
    temperature = round(daily_data['temp'].values[0] * 41, 1)  # Normalisasi suhu
    humidity = round(daily_data['hum'].values[0] * 100, 1)  # Kelembaban dalam %
    windspeed = round(daily_data['windspeed'].values[0] * 67, 1)  # Normalisasi kecepatan angin

    col2.metric("Kondisi Cuaca", weather)
    st.info(f" Suhu: {temperature}°C  |  Kelembaban: {humidity}%  |  Angin: {windspeed} km/jam")

    st.subheader(" Grafik Penyewaan Harian")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=["Casual", "Registered", "Total"], y=[
        daily_data['casual'].values[0],
        daily_data['registered'].values[0],
        daily_data['cnt'].values[0]
    ], palette="coolwarm", ax=ax)
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

    st.subheader(" Tren Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x='dteday', y='cnt', marker='o', label="Total Rentals", ax=ax)
    plt.axvline(pd.to_datetime(selected_date), color='r', linestyle='--', label="Selected Date")
    plt.xticks(rotation=45)
    plt.xlabel("Tanggal")
    plt.ylabel("Total Peminjaman")
    plt.legend()
    st.pyplot(fig)

else:
    st.warning(" Tidak ada data untuk tanggal ini. Silakan pilih tanggal lain.")

st.subheader(" Hari dengan Penyewaan Tertinggi & Terendah")

max_day = df.loc[df['cnt'].idxmax()]
min_day = df.loc[df['cnt'].idxmin()]

col1, col2 = st.columns(2)

col1.metric(" Penyewaan Tertinggi", f"{max_day['cnt']} sepeda", f"Pada {max_day['dteday'].date()}")
col2.metric(" Penyewaan Terendah", f"{min_day['cnt']} sepeda", f"Pada {min_day['dteday'].date()}")
