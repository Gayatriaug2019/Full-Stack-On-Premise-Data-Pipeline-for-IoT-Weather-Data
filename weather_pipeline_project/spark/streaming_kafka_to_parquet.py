from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("KafkaToParquet").getOrCreate()

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "weather-topic") \
    .option("failOnDataLoss", "false") \
    .option("startingOffsets", "latest") \
    .load()

df.selectExpr("CAST(value AS STRING)").writeStream \
    .format("parquet") \
    .option("path", "file:///root/weather_pipeline_project/csv_parquet_storage/parquet_output") \
    .option("checkpointLocation", "file:///root/weather_pipeline_project/csv_parquet_storage/checkpoint") \
    .trigger(processingTime="300 seconds") \
    .start().awaitTermination()
