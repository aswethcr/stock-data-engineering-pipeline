import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Real-Time Stock Analytics", layout="wide")

# auto refresh every 5 seconds
st_autorefresh(interval=5000)

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="stockdb",
    user="aswethcr",
    password="postgres"
)

query = "SELECT * FROM stock_prices ORDER BY timestamp"
df = pd.read_sql(query, conn)
st.subheader("Pipeline Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(df))
col2.metric("Max Price", df["price"].max())
col3.metric("Min Price", df["price"].min())
col4.metric("Average Price", round(df["price"].mean(), 2))

st.subheader("Records Per Stock")

stock_counts = df["symbol"].value_counts()

st.bar_chart(stock_counts)

if df.empty:
    st.warning("No data available yet.")
    st.stop()

st.title("📊 Real-Time Stock Data Engineering Dashboard")

# -------- KPI METRICS -------- #

col1, col2, col3, col4 = st.columns(4)

col1.metric("Current Price", f"${df['price'].iloc[-1]:.2f}")
col2.metric("Average Price", f"${df['price'].mean():.2f}")
col3.metric("Max Price", f"${df['price'].max():.2f}")
col4.metric("Total Trades", len(df))

st.divider()

# -------- PRICE TREND -------- #

st.subheader("📈 Price Trend")

price_chart = px.line(
    df,
    x="timestamp",
    y="price",
    title="Stock Price Over Time",
    markers=True
)

st.plotly_chart(price_chart, use_container_width=True)

# -------- VOLUME + DISTRIBUTION -------- #

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Trading Volume")

    volume_chart = px.bar(
        df,
        x="timestamp",
        y="volume",
        title="Volume per Trade"
    )

    st.plotly_chart(volume_chart, use_container_width=True)

with col2:
    st.subheader("📉 Price Distribution")

    hist = px.histogram(
        df,
        x="price",
        nbins=20,
        title="Price Distribution"
    )

    st.plotly_chart(hist, use_container_width=True)

st.divider()

# -------- FILTER -------- #

st.subheader("🔍 Data Filter")

min_price, max_price = st.slider(
    "Filter by Price Range",
    float(df.price.min()),
    float(df.price.max()),
    (float(df.price.min()), float(df.price.max()))
)

filtered_df = df[(df.price >= min_price) & (df.price <= max_price)]

# -------- TABLE -------- #

st.subheader("📄 Streaming Data Table")

st.dataframe(filtered_df, use_container_width=True)