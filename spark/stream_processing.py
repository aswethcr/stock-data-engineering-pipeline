from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Stock Data Processing") \
    .getOrCreate()

df = spark.read.json("data_lake/raw/stock_data.json")

df.show()

df.write.csv("data_lake/processed/stock_cleaned.csv", header=True)

spark.stop()