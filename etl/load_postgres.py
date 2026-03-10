import pandas as pd
import psycopg2

# read processed data
df = pd.read_csv("data_lake/processed/stock_cleaned.csv")

conn = psycopg2.connect(
    host="localhost",
    database="stockdb",
    user="aswethcr",
    password=""
)

cursor = conn.cursor()

for _, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO stock_prices (symbol, price, volume, timestamp)
        VALUES (%s,%s,%s,%s)
        """,
        (row["symbol"], row["price"], row["volume"], row["timestamp"])
    )

conn.commit()

print("Data loaded into PostgreSQL")