#!/bin/bash

echo "Starting Kafka Producer..."
python3 kafka/producer.py &

sleep 3

echo "Starting Kafka Consumers..."
python3 kafka/consumer.py &
python3 kafka/consumer.py &
python3 kafka/consumer.py &

sleep 5

echo "Running Spark Processing..."
python3 spark/stream_processor.py &

sleep 5

echo "Running ETL Transform..."
python3 etl/transform.py &

sleep 2

echo "Loading Data to PostgreSQL..."
python3 etl/load_postgres.py &

sleep 2

echo "Starting Dashboard..."
streamlit run dashboard/app.py --server.address=0.0.0.0 --server.port=8501 &
wait