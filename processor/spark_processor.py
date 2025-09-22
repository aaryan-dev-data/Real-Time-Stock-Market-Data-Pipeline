from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, avg, max as spark_max, min as spark_min, sum as spark_sum, window

spark = SparkSession.builder.appName("StockProcessor").getOrCreate()

# Read from Pub/Sub subscription
df = spark.read.format("pubsub") \
    .option("project", "your-gcp-project") \
    .option("subscription", "projects/your-gcp-project/subscriptions/stock-sub") \
    .load()

# Transform
df = df.withColumn("timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss"))

df_features = df.groupBy(
    window(col("timestamp"), "5 minutes"),
    col("symbol")
).agg(
    avg("price").alias("avg_price"),
    spark_max("high").alias("max_price"),
    spark_min("low").alias("min_price"),
    spark_sum("volume").alias("total_volume")
)

# Write to BigQuery
df_features.write.format("bigquery") \
    .option("table", "your-gcp-project.stock_dataset.stock_prices") \
    .save()
