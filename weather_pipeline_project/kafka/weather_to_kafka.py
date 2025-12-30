import requests, json, time
from kafka import KafkaProducer

API_KEY = ''
CITY = 'Delhi'
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    response = requests.get(URL).json()
    print("Response*****  ",response)
    producer.send('weather-topic', response)
    time.sleep(60)
