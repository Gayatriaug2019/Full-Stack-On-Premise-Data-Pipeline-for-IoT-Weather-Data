# 🌦️ Full-Stack On-Premise Data Pipeline for IoT & Weather Data

## 📌 Project Overview
This project implements a **full-stack, on-premise data engineering pipeline** for a hypothetical **Weather Analytics Company**.  
The pipeline ingests **real-time weather data**, generates **synthetic IoT and user data**, processes both **streaming and batch workloads**, and stores results across **data lake, relational, and analytical systems**.

The solution demonstrates **end-to-end data engineering skills**, including ingestion, processing, storage, orchestration, monitoring, and containerization.

---

## 🧠 Skills Gained from This Project
- Python  
- SQL  
- MongoDB  
- Apache Kafka  
- Apache Spark (Streaming & Batch)  
- Apache Hive  
- Apache Sqoop  
- Apache Airflow  
- Docker & Docker Compose  

---

## 🏭 Domain
**Weather Analytics & IoT Data Processing**

---

## 🎯 Problem Statement
You are tasked with building an **on-premise data engineering pipeline** that:
- Ingests real-time weather data from a public API
- Generates synthetic data using Faker
- Handles both streaming and batch processing
- Stores data across Hive, MySQL, and Parquet
- Orchestrates workflows using Airflow
- (Optional) Containerizes the full system using Docker Compose

---

## 🛠️ Technology Stack & Purpose

| Technology | Purpose |
|---------|---------|
| Apache Kafka | Real-time data ingestion |
| Apache Spark | Streaming & Batch Processing |
| Apache Hive | Data Lake / Analytical Tables |
| MySQL | Relational Storage |
| Apache Airflow | Workflow Orchestration |
| Docker Compose | Infrastructure Setup |
| Python | Data ingestion & ETL logic |

---

## 📂 Project Structure
weather-data-pipeline/
│
├── airflow/
│   ├── dags/
│   │   ├── batch_etl_dag.py
│   │   ├── faker_csv_dag.py
│   │   ├── faker_mysql_dag.py
│   │   └── weather_to_kafka_dag.py
│
├── kafka/
│ └── weather_to_kafka.py
│
├── faker/
│   ├── generate_csv.py
│   └── insert_fake_mysql.py
│
├── spark/
│ ├── streaming_kafka_to_parquet.py
│ ├── batch_etl.py
│ └── last_etl_timestamp.txt
│
├── csv_parquet_storage/
│   ├── fake_weather.csv
│   │
│   ├── parquet_output/
│   │   └── part-00000-6dd5899c-d930-479c-ac12-4dbb4f9808ba-c000.snappy.parquet
│   │
│   └── hive_final_table_export/
│       └── part-00000-6ddcee01-6085-4af2-acc9-894bd7b5b796-c000.csv
├── hive/
│ └── create_hive_tables.sql
│
├── docker/
│ └── docker-compose.yml # Optional
│
└── README.md

---

## 🔄 Pipeline Architecture Overview

### 1️⃣ Ingestion Layer
#### Weather API ➜ Kafka
- Fetches real-time weather data from **OpenWeatherMap API**
- Data is pushed to Kafka topic:
weather-topic

- Scheduled every minute using **Airflow DAG**

#### Faker ➜ CSV
- Generates synthetic user weather logs (Name, City, Temperature)
- Writes CSV files every minute

#### Faker ➜ MySQL
- Generates mock IoT sensor/device data
- Inserts records into MySQL table

---

### 2️⃣ Processing Layer
#### Spark Streaming
- Consumes data from Kafka topic
- Writes processed output as **Parquet files**
- Trigger interval: **every 5 minutes**

#### Spark Batch ETL
- Reads:
- CSV files (Faker-generated)
- MySQL tables (sensor/device data)
- Performs transformations:
- Join
- Filter
- Select
- Loads results into:
- Hive Table (`final_table`)
- MySQL Table (`final_table`)

---

### 3️⃣ Storage Layer
- **Parquet Files** → Kafka streaming output
- **Hive Tables** → Analytical data lake
- **MySQL Tables** → Relational serving layer

---

### 4️⃣ Orchestration
- **Apache Airflow** orchestrates:
- Weather API ingestion
- Kafka producers
- Spark batch ETL jobs

---

### 5️⃣ Monitoring & Observability
- Pipeline health
- Job execution
- Resource utilization
- (Optional) Monitor Airflow, Spark, and Docker containers

---

## ▶️ How to Run the Project

### Prerequisites
- Python 3.x
- Apache Kafka
- Apache Spark
- Apache Hive
- MySQL
- Apache Airflow
- Docker & Docker Compose (optional)

---

### Step 1: Start Kafka Producer
bash
python kafka/weather_producer.py

Step 2: Run Faker Data Generators
bash
python faker/faker_to_csv.py
python faker/faker_to_mysql.py

Step 3: Start Airflow
Enable DAGs:
weather_to_kafka_dag
batch_etl_dag

Step 4: Run Spark Jobs
bash
spark-submit spark/streaming_kafka_to_parquet.py
spark-submit spark/batch_etl.py

📊 Results & Deliverables
Each submission includes:
Project Code Repository

Airflow DAGs
weather_to_kafka_dag.py
batch_etl_dag.py

Spark Jobs
streaming_kafka_to_parquet.py
batch_etl.py

Docker Compose File (Optional)

Hive SQL Scripts

README.md (This file)

👤 Author
Gayatri
Python Backend Engineer | Data Engineer
