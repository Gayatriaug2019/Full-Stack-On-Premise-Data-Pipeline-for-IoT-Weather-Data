from pyspark.sql import SparkSession
from datetime import datetime
import mysql.connector
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("BatchETL") \
    .config("hive.metastore.uris", "thrift://localhost:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# Read last ETL timestamp
try:
    with open("/root/weather_pipeline_project/spark/last_etl_timestamp.txt", "r") as f:
        last_etl_time = f.read().strip()
except FileNotFoundError:
    last_etl_time = "2000-01-01T00:00:00"

# Step 1: Ensure Hive table exists
spark.sql("""
CREATE TABLE IF NOT EXISTS final_table (
    name STRING,
    city STRING,
    temperature FLOAT,
    device_id STRING,
    status STRING,
    created_at TIMESTAMP
)
STORED AS PARQUET
""")

# Step 2: Ensure MySQL table exists
conn = mysql.connector.connect(user='airflow', password='your_password', host='localhost')
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS weather_db")
cursor.execute("USE weather_db")
cursor.execute("""
CREATE TABLE IF NOT EXISTS final_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(100),
    temperature FLOAT,
    device_id VARCHAR(255),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
cursor.close()
conn.close()

# Step 3: Read and filter CSV
csv_df = spark.read.csv("file:///root/weather_pipeline_project/csv_parquet_storage/fake_weather.csv", header=False)
csv_df = csv_df.withColumnRenamed("_c0", "name") \
               .withColumnRenamed("_c1", "city") \
               .withColumnRenamed("_c2", "temperature") \
               .withColumnRenamed("_c3", "created_at")

filtered_csv = csv_df.filter(f"created_at > '{last_etl_time}'").alias("csv")
print("Filtered CSV rows:", filtered_csv.count())

# Step 4: Read and filter MySQL
mysql_df = spark.read.format("jdbc").options(
    url="jdbc:mysql://localhost/weather_db?useSSL=false&serverTimezone=UTC",
    driver="com.mysql.cj.jdbc.Driver",
    dbtable="sensors",
    user="airflow",
    password="your_password").load()

filtered_mysql = mysql_df.filter(f"created_at > '{last_etl_time}'").alias("mysql")
print("Filtered MySQL rows:", filtered_mysql.count())

# Add these lines to inspect join keys

filtered_csv.select("city").distinct().show()
filtered_mysql.select("location").distinct().show()

# Step 5: Join and transform
joined_df = filtered_csv.join(filtered_mysql, filtered_csv["city"] == filtered_mysql["location"])
transformed_df = joined_df.select(
    col("csv.name"),
    col("csv.city"),
    col("csv.temperature").cast("float"),
    col("mysql.device_id"),
    col("mysql.status"),
    col("mysql.created_at")
)

print("Transformed row count:", transformed_df.count())

# Step 6: Append to Hive and MySQL
transformed_df.write.insertInto("final_table", overwrite=False)
transformed_df.write.format("jdbc").options(
    url="jdbc:mysql://localhost/weather_db?useSSL=false&serverTimezone=UTC",
    driver="com.mysql.cj.jdbc.Driver",
    dbtable="final_table",
    user="airflow",
    password="your_password").mode("append").save()

print("Exporting Hive table to CSV...")

# Step 7: Export Hive table to CSV

hive_df = spark.sql("SELECT * FROM final_table")
#hive_df.write.mode("overwrite").csv("/root/weather_pipeline_project/csv_parquet_storage/hive_final_table_export", header=True)
try:
    hive_df.write.mode("overwrite").csv("file:///root/weather_pipeline_project/csv_parquet_storage/hive_final_table_export", header=True)
    print(" Hive table exported to CSV.")
except Exception as e:
    print(" CSV export failed:", e)


# Step 8: Update ETL timestamp
with open("/root/weather_pipeline_project/spark/last_etl_timestamp.txt", "w") as f:
    f.write(datetime.now().isoformat())



