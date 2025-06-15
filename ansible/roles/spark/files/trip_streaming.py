from pyspark.sql import SparkSession
import os

kafka_server = os.environ["KAFKA_BOOTSTRAP_SERVERS"]

spark = SparkSession.builder \
    .appName("TripStreamSQL") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_server) \
    .option("subscribe", "trip_start,trip_end") \
    .option("startingOffsets", "latest") \
    .load()

from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StringType, IntegerType

schema = StructType() \
    .add("type", StringType()) \
    .add("timestamp", StringType()) \
    .add("PULocationID", IntegerType()) \
    .add("DOLocationID", IntegerType())

parsed_df = df.selectExpr("CAST(value AS STRING) AS json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select(
    to_timestamp(col("data.timestamp")).alias("event_time"),
    col("data.PULocationID"),
    col("data.DOLocationID")
) \
    .withWatermark("event_time", "1 hour")

parsed_df.createOrReplaceTempView("trips")

# Run SQL query to count trips between zone pairs by hour
result_df = spark.sql("""
                      SELECT PULocationID,
                             DOLocationID,
                             window(event_time, '1 hour') as trip_hour,
                             COUNT(*)                     as trip_count
                      FROM trips
                      GROUP BY window(event_time, '1 hour'), PULocationID, DOLocationID
                      """)

output_dir = os.getenv("OUTPUT_DIR", "/opt/output")

query = result_df.writeStream \
    .format("parquet") \
    .option("path", "/opt/output/hourly_trip_counts") \
    .option("checkpointLocation", "/tmp/trip_counts") \
    .outputMode("append") \
    .start()

query.awaitTermination()
