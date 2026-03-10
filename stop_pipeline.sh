#!/bin/bash

echo "Stopping pipeline..."

pkill -f producer.py
pkill -f consumer.py
pkill -f stream_processor.py
pkill -f transform.py
pkill -f load_postgres.py
pkill -f streamlit

echo "Pipeline stopped."