import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style='dark')

def workingday_df(df):
    working_data = df.groupby('workingday_daily')['cnt_daily'].count().reset_index()
    working_data.loc[working_data["workingday_daily"] == 0, "workingday_daily"] = "Holiday"
    working_data.loc[working_data["workingday_daily"] == 1, "workingday_daily"] = "Working Day"
    working_data.rename(columns={"cnt_daily": "sum"}, inplace=True)
    return working_data

def season_df(df):
    seasonal_data_daily = df.groupby('season_daily')['cnt_daily'].count().reset_index()
    seasonal_data_daily.loc[seasonal_data_daily["season_daily"] == 1, "season_daily"] = "Spring"
    seasonal_data_daily.loc[seasonal_data_daily["season_daily"] == 2, "season_daily"] = "Summer"
    seasonal_data_daily.loc[seasonal_data_daily["season_daily"] == 3, "season_daily"] = "Fall"
    seasonal_data_daily.loc[seasonal_data_daily["season_daily"] == 4, "season_daily"] = "Winter"
    seasonal_data_daily.rename(columns={"cnt_daily": "sum"}, inplace=True)
    return seasonal_data_daily

def weather_df(df):
    weathersit_data_daily = df.groupby('weathersit_daily')['cnt_daily'].count().reset_index()
    weathersit_data_daily.loc[weathersit_data_daily["weathersit_daily"] == 1, "weathersit_daily"] = "Clear"
    weathersit_data_daily.loc[weathersit_data_daily["weathersit_daily"] == 2, "weathersit_daily"] = "Mist + Cloudy"
    weathersit_data_daily.loc[weathersit_data_daily["weathersit_daily"] == 3, "weathersit_daily"] = "Light Snow"
    weathersit_data_daily.rename(columns={"cnt_daily": "sum"}, inplace=True)
    return weathersit_data_daily

def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    with st.sidebar:
        # Menambahkan logo 
        st.image("https://www.brandcrowd.com/blog/wp-content/uploads/2019/06/bike-share.png")

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )
        

    return date

# load dataset
bike_sharing = pd.read_csv("https://raw.githubusercontent.com/kharismaKD74/Dicoding-Analysis-Bike-Sharing/main/dashboard/bike_sharing.csv?token=GHSAT0AAAAAACK5SCNNNLFM2WAPWYNWODB4ZLHEUBA")

date = sidebar(bike_sharing)
if len(date) == 2:
    main_df = bike_sharing[(bike_sharing["dteday"] >= str(date[0])) & (bike_sharing["dteday"] <= str(date[1]))]
else:
    main_df = bike_sharing[
        (bike_sharing["dteday"] >= str(st.session_state.date[0])) & (bike_sharing["dteday"] <= str(st.session_state.date[1]))]

working_data = workingday_df(main_df)
seasonal_data_daily = season_df(main_df)
weathersit_data_daily = weather_df(main_df)

# Title
st.title("Bike Sharing Dashboard :bike:")
st.markdown("##")

total = int(main_df["cnt_daily"].sum())
average = round(main_df["cnt_daily"].mean())

left_column, middle_column = st.columns(2)
with left_column:
    st.subheader("Total Sewa:")
    st.subheader(f"{total:,}")
with middle_column:
    st.subheader("Rata-rata Sewa Perhari:")
    st.subheader(f"{average}")

st.markdown("""---""")
colors = ["#2196f3", "#2196f3", "#2196f3", "#2196f3", "#2196f3"]

# pengaruh hari kerja mempengeruhi pengunaan bike sharing
st.subheader("Pengaruh Hari Kerja dan Holiday Terhadap Jumlah Sewa Sepeda Harian")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="workingday_daily",
    y="sum",
    data=working_data.sort_values(by="workingday_daily", ascending=True), palette=colors,
    ax=ax
)
ax.set_ylabel("Jumlah Sewa Harian",fontsize=30)
ax.set_xlabel("Kategori Hari",fontsize=30)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# kondisi musim terhadap banyaknya pengguna bike sharing
st.subheader("Pengaruh Musim Terhadap Jumlah Sewa Sepeda Harian")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="sum",
    x="season_daily",
    data=seasonal_data_daily.sort_values(by="season_daily", ascending=False), palette=colors,
)
ax.set_ylabel("Jumlah Sewa Harian",fontsize=30)
ax.set_xlabel("Musim",fontsize=30)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# kondisi cuaca terhadap banyaknya pengguna bike sharing
st.subheader("Pengaruh Cuaca Terhadap Jumlah Sewa Sepeda Harian")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="sum",
    x="weathersit_daily",
    data=weathersit_data_daily.sort_values(by="weathersit_daily", ascending=False), palette=colors,
)
ax.set_ylabel("Jumlah Sewa Harian",fontsize=30)
ax.set_xlabel("Cuaca",fontsize=30)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Pola berdasarkan bulan
st.subheader("Pola Jumlah Sewa Sepeda Harian Berdasarkan Bulan")
fig, ax = plt.subplots(figsize=(20, 10))
sns.lineplot(
    x="mnth_daily",
    y="cnt_daily",
    data=main_df.sort_values(by="mnth_daily", ascending=False),
    ax=ax
)
ax.set_ylabel("Jumlah Sewa Harian",fontsize=30)
ax.set_xlabel("Bulan",fontsize=30)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

st.subheader("Pola Jumlah Sewa Sepeda Harian Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(20, 10))
sns.lineplot(
    x="hr",
    y="cnt_hourly",
    data=main_df.sort_values(by="hr", ascending=False),
    ax=ax
)
ax.set_ylabel("Jumlah Sewa Harian",fontsize=30)
ax.set_xlabel("Jam",fontsize=30)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

st.caption('Copyright (c) Kharisma 2023')
