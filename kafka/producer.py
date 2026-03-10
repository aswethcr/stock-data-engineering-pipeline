import json
import time
import random
import logging
from datetime import datetime
from kafka import KafkaProducer

# ---------------------------
# Logging configuration
# ---------------------------
logging.basicConfig(
    filename="producer.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s"
)

# ---------------------------
# Kafka Producer setup
# ---------------------------
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Stock Producer Started...")

# ---------------------------
# Multi-stock list
# ---------------------------
stocks = {
    "AAPL": 190.0,
    "TSLA": 240.0,
    "GOOG": 130.0,
    "MSFT": 320.0,
    "AMZN": 140.0
}

# ---------------------------
# Streaming loop
# ---------------------------
while True:

    try:

        # randomly select stock
        symbol = random.choice(list(stocks.keys()))

        # simulate price movement
        price = round(stocks[symbol] + random.uniform(-2, 2), 2)
        stocks[symbol] = price

        data = {
            "symbol": symbol,
            "price": price,
            "volume": random.randint(1000, 10000),
            "timestamp": datetime.now().isoformat()
        }

        producer.send("stock-topic", data)

        print("Sent:", data)
        logging.info("Data sent: %s", data)

        time.sleep(3)

    except Exception as e:

        logging.error("Producer error: %s", e)
        print("Error:", e)
        time.sleep(3)