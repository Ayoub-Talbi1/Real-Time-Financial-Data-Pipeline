from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Create a SparkSession
spark = SparkSession.builder.appName("KafkaStreamProcessing").getOrCreate()

# Add the Cassandra connector library
spark.sparkContext.addPyFile("https://repo1.maven.org/maven2/com/datastax/spark/spark-cassandra-connector_2.12/3.1.0/spark-cassandra-connector_2.12-3.1.0.jar")

# Define the schema to match the JSON structure
schema = StructType([
    StructField("id", StringType(), True),
    StructField("exchange", StringType(), True),
    StructField("quoteType", DoubleType(), True),
    StructField("price", DoubleType(), True),
    StructField("timestamp", DoubleType(), True),
    StructField("marketHours", DoubleType(), True),
    StructField("changePercent", DoubleType(), True),
    StructField("dayVolume", DoubleType(), True),
    StructField("change", DoubleType(), True),
    StructField("priceHint", DoubleType(), True)
])

# Read data from Kafka as a streaming DataFrame
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-container:9092") \
    .option("subscribe", "yfinance") \
    .load()

# Parse the JSON data
parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json("json", schema).alias("data")) \
    .select("data.*")

# Group by 'id' and calculate cumulative average of 'price'
result_df = parsed_df.groupBy("id") \
    .agg({"price": "avg"}) \
    .withColumnRenamed("avg(price)", "cumulative_avg_price")

# Function to write data to Cassandra
def write_to_cassandra(df, epoch_id):
    df.write \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="yahoofinance", keyspace="streams") \
        .mode("append") \
        .option("spark.cassandra.connection.host", "cassandra-container") \
        .option("spark.cassandra.connection.port", "9042") \
        .save()

# Write data to Cassandra using the foreach sink
query = result_df.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_cassandra) \
    .start()

# Wait for the streaming query to terminate
query.awaitTermination()
