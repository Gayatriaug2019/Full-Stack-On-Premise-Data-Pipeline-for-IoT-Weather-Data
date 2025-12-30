import mysql.connector
from faker import Faker
import time
import random

conn = mysql.connector.connect(user='airflow', password='your_password', host='localhost')
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS weather_db")
cursor.execute("USE weather_db")
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(255),
    location VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

fake = Faker()
cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"]

while True:
    cursor.execute("INSERT INTO sensors (device_id, location, status) VALUES (%s, %s, %s)",
                   (fake.uuid4(), random.choice(cities), random.choice(['active', 'inactive'])))
    conn.commit()
    time.sleep(60)
