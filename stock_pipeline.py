import psycopg2
import yfinance as yf

conn = psycopg2.connect(
    host="aws-1-ap-northeast-2.pooler.supabase.com",
    database="postgres",
    user="postgres.liexaqlhycxrqbtwdgki",
    password="Asweth0810@rx",
    port=5432
)

cur = conn.cursor()

data = yf.Ticker("AAPL").history(period="1mo")

for index, row in data.iterrows():
    cur.execute(
        "INSERT INTO stock_prices (symbol, price, volume, timestamp) VALUES (%s,%s,%s,%s)",
        ("AAPL", float(row["Close"]), float(row["Volume"]), index)
    )

conn.commit()

print("Stock data inserted successfully")