import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="London Bike Sharing Dashboard", layout="wide")

st.title("🚲 London Bike Sharing Analysis")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("london_merged.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["month"] = df["timestamp"].dt.month
    df["day"] = df["timestamp"].dt.day_name()
    return df

df = load_data()

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filters")

season = st.sidebar.multiselect(
    "Select Season",
    options=df["season"].unique(),
    default=df["season"].unique()
)

df = df[df["season"].isin(season)]

# ----------------------------
# KPI METRICS
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", int(df["cnt"].sum()))
col2.metric("Average Temperature", round(df["t1"].mean(),2))
col3.metric("Average Wind Speed", round(df["wind_speed"].mean(),2))

st.divider()

# ----------------------------
# RIDES OVER TIME
# ----------------------------
st.subheader("Bike Rentals Over Time")

fig = px.line(
    df,
    x="timestamp",
    y="cnt",
    title="Bike Rentals Trend"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# RENTALS BY HOUR
# ----------------------------
st.subheader("Rentals by Hour")

hourly = df.groupby("hour")["cnt"].mean().reset_index()

fig2 = px.bar(
    hourly,
    x="hour",
    y="cnt",
    title="Average Rentals by Hour"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# WEEKEND VS WEEKDAY
# ----------------------------
st.subheader("Weekend vs Weekday Usage")

weekend = df.groupby("is_weekend")["cnt"].mean().reset_index()

fig3 = px.bar(
    weekend,
    x="is_weekend",
    y="cnt",
    title="Average Rentals"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# WEATHER IMPACT
# ----------------------------
st.subheader("Temperature vs Rentals")

fig4 = px.scatter(
    df,
    x="t1",
    y="cnt",
    title="Temperature vs Rentals",
    opacity=0.5
)

st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# CORRELATION HEATMAP
# ----------------------------
st.subheader("Correlation Heatmap")

corr = df.drop(columns=["timestamp","day"]).corr()

fig5, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig5)