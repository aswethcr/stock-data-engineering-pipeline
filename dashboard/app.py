import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import yfinance as yf

st.set_page_config(page_title="Real-Time Stock Analytics", layout="wide")

# Auto refresh every 5 seconds
st_autorefresh(interval=5000)

st.title("📊 Real-Time Stock Data Engineering Dashboard")

# -------- DATABASE CONNECTION -------- #

try:
    conn = psycopg2.connect(
        host="localhost",
        database="stockdb",
        user="aswethcr",
        password="postgres"
    )

    query = "SELECT * FROM stock_prices ORDER BY timestamp"
    df = pd.read_sql(query, conn)

    st.success("Connected to PostgreSQL database")

except Exception:

    st.warning("Database not available. Running in demo mode.")

    # Demo stock data for Streamlit Cloud
    demo = yf.download("AAPL", period="1d", interval="1m")
    demo.reset_index(inplace=True)

    df = pd.DataFrame({
        "timestamp": demo["Datetime"],
        "price": demo["Close"],
        "volume": demo["Volume"],
        "symbol": "AAPL"
    })

# -------- PIPELINE METRICS -------- #

st.subheader("Pipeline Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(df))
col2.metric("Max Price", round(df["price"].max(), 2))
col3.metric("Min Price", round(df["price"].min(), 2))
col4.metric("Average Price", round(df["price"].mean(), 2))

# -------- RECORDS PER STOCK -------- #

st.subheader("Records Per Stock")

stock_counts = df["symbol"].value_counts()

st.bar_chart(stock_counts)

if df.empty:
    st.warning("No data available yet.")
    st.stop()

st.divider()

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

# -------- DATA TABLE -------- #

st.subheader("📄 Streaming Data Table")

st.dataframe(filtered_df, use_container_width=True)