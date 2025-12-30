from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime , timedelta

default_args = {
    'owner': 'gayatri',
    'start_date': datetime.now() - timedelta(days=1),  # replaces days_ago(1)
    'retries': 1,
}

with DAG(
    dag_id='faker_csv_dag',
    default_args=default_args,
    schedule='* * * * *',  # runs every minute
    catchup=False,
) as dag:

    generate_csv = BashOperator(
        task_id='generate_fake_csv',
        bash_command='/root/.local/share/pipx/venvs/apache-airflow/bin/python /root/weather_pipeline_project/faker/generate_csv.py',
    )

