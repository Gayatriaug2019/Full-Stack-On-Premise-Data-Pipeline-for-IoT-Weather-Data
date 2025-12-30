from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'gayatri',
    'start_date': datetime.now() - timedelta(days=1),  # replaces days_ago(1)
    'retries': 1,
}

with DAG(
    dag_id='weather_to_kafka',
    default_args=default_args,
    schedule='* * * * *',  # runs every minute
    catchup=False,
) as dag:

    task = BashOperator(
        task_id='push_weather_to_kafka',
        bash_command='/root/.local/share/pipx/venvs/apache-airflow/bin/python /root/weather_pipeline_project/kafka/weather_to_kafka.py',
    )

