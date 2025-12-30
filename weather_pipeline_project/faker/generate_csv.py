import csv, time
from faker import Faker
import random
from datetime import datetime

fake = Faker()
csv_path = '/root/weather_pipeline_project/csv_parquet_storage/fake_weather.csv'

# Shared city pool
cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"]

while True:
    with open(csv_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            fake.name(),
            random.choice(cities),
            round(random.uniform(20, 40), 2),
            datetime.now().isoformat()
        ])
    time.sleep(60)
