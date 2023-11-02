import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_style("dark")


### Menyiapkan DataFrame
def create_monthly_users_df(df):
    monthly_users_df = df.resample(
        rule="M",
        on="dteday",
    ).agg(
        {
            "casual": "sum",
            "registered": "sum",
            "cnt": "sum",
        }
    )
    monthly_users_df.index = monthly_users_df.index.strftime("%b-%Y")
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(
        columns={
            "dteday": "tanggal",
            "cnt": "jumlah",
            "casual": "kasual",
            "registered": "terdaftar",
        },
        inplace=True,
    )

    return monthly_users_df


def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hr").agg(
        {
            "casual": "sum",
            "registered": "sum",
            "cnt": "sum",
        }
    )
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(
        columns={
            "cnt": "jumlah",
            "casual": "kasual",
            "registered": "terdaftar",
        },
        inplace=True,
    )

    return hourly_users_df


df = pd.read_csv("hour_cleaned.csv")
df.reset_index(inplace=True)
df["dteday"] = pd.to_datetime(df["dteday"])


### Membuat Komponen Filter
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    st.image(
        "https://play-lh.googleusercontent.com/ot77md7kXTjxL5TCNnQVtIoTVi2Y1N8t_0hp4FJ_gg4-RSDrrsa_bCjZZc9qqn9rdm0i"
    )

    start_date, end_date = st.date_input(  # type: ignore
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[
            min_date,
            max_date,
        ],
    )

main_df = df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date))]

monthly_users_df = create_monthly_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)


### Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header("Bike-Sharing Dashboard :bar_chart:")
col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df["cnt"].sum()
    st.metric(label="Jumlah Pengguna", value=total_all_rides)

with col2:
    total_casual_rides = main_df["casual"].sum()
    st.metric(label="Jumlah Pengguna Kasual", value=total_casual_rides)

with col3:
    total_registered_rides = main_df["registered"].sum()
    st.metric(label="Jumlah Pengguna Terdaftar", value=total_registered_rides)

st.markdown("---")


fig, ax = plt.subplots(figsize=(20, 10))

sns.lineplot(
    data=monthly_users_df,
    x="tanggal",
    y="jumlah",
    color="red",
    label="Total",
    ax=ax,
)
sns.lineplot(
    data=monthly_users_df,
    x="tanggal",
    y="kasual",
    color="blue",
    label="Kasual",
    ax=ax,
)
sns.lineplot(
    data=monthly_users_df,
    x="tanggal",
    y="terdaftar",
    color="darkblue",
    label="Terdaftar",
    ax=ax,
)

ax.set_title("Jumlah Pengguna Layanan Bike-Sharing", fontsize=33)
ax.set_ylabel(None)
ax.set_xlabel(None)
plt.xticks(rotation=45)

st.pyplot(fig)


fig, ax = plt.subplots(figsize=(20, 10))

sns.lineplot(
    data=hourly_users_df,
    x="hr",
    y="kasual",
    color="blue",
    label="Kasual",
    ax=ax,
)
sns.lineplot(
    data=hourly_users_df,
    x="hr",
    y="terdaftar",
    color="darkblue",
    label="Terdaftar",
    ax=ax,
)

x = np.arange(0, 24, 1)
plt.xticks(x)

plt.axvline(x=8, color="gray", linestyle="dashed")
plt.axvline(x=17, color="gray", linestyle="dashed")

ax.set_title(
    "Jumlah Penggunaan Layanan Bike-Sharing Berdasarkan Waktu dalam Sehari", fontsize=33
)
ax.set_ylabel(None)
ax.set_xlabel(None)

st.pyplot(fig)


fig, ax = plt.subplots(figsize=(15, 10))

sns.scatterplot(
    data=df,
    x="temp",
    y="cnt",
    hue="season",
    palette="deep",
    ax=ax,
)

ax.set_title(
    "Jumlah Penggunaan Layanan Bike-Sharing Berdasarkan Musim dan Suhu", fontsize=33
)
ax.set_xlabel("Suhu (°C)")
ax.set_ylabel(None)

st.pyplot(fig)


st.caption("Copyright (c) Dicoding 2023, Modified by Besar Rachmat Ikhsan Pambudi")
