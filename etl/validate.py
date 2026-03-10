import pandas as pd

df = pd.read_csv("data_lake/processed/stock_cleaned.csv")

invalid_records = df[(df["price"] <= 0) | (df["volume"] <= 0)]

if len(invalid_records) > 0:
    print("Invalid records found")
    print(invalid_records)
else:
    print("Data validation passed")