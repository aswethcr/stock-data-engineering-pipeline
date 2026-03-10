import json
import pandas as pd

input_file = "data_lake/raw/stock_data.json"
output_file = "data_lake/processed/stock_cleaned.csv"

records = []

with open(input_file, "r") as f:
    for line in f:
        data = json.loads(line)

        # basic validation
        if data["price"] > 0 and data["volume"] > 0:
            records.append(data)

df = pd.DataFrame(records)

# convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

df.to_csv(output_file, index=False)

print("Transformation complete")
print(df.head())