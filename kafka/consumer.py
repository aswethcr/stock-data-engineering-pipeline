from kafka import KafkaConsumer
import json
import psycopg2
import logging
import pathlib

# -----------------------
# Logging Configuration
# -----------------------
logging.basicConfig(
    filename="consumer.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s"
)

# -----------------------
# PostgreSQL Connection
# -----------------------
conn = psycopg2.connect(
    host="localhost",
    database="stockdb",
    user="aswethcr",
    password=""
)

cursor = conn.cursor()

# -----------------------
# Kafka Consumer Setup
# -----------------------
consumer = KafkaConsumer(
    "stock-topic",
    bootstrap_servers="localhost:9092",
    group_id="stock-consumer-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Consumer started...")

# -----------------------
# Ensure Data Lake Folder Exists
# -----------------------
pathlib.Path("data_lake/raw").mkdir(parents=True, exist_ok=True)

# -----------------------
# Start Consuming
# -----------------------
for message in consumer:

    data = message.value

    try:

        # -----------------------
        # Data Validation
        # -----------------------
        if data["price"] <= 0:
            logging.warning("Invalid price detected: %s", data)
            continue

        if data["volume"] <= 0:
            logging.warning("Invalid volume detected: %s", data)
            continue

        print("Received:", data)
        logging.info("Data received: %s", data)

        # -----------------------
        # Store Raw Data in Data Lake
        # -----------------------
        with open("data_lake/raw/stock_data.json", "a") as f:
            f.write(json.dumps(data) + "\n")

        # -----------------------
        # Insert into PostgreSQL
        # -----------------------
        cursor.execute(
            """
            INSERT INTO stock_prices (symbol, price, volume, timestamp)
            VALUES (%s,%s,%s,%s)
            """,
            (
                data["symbol"],
                data["price"],
                data["volume"],
                data["timestamp"]
            )
        )

        conn.commit()

    except Exception as e:

        logging.error("Error processing record: %s", e)
        print("Error:", e)