from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime , timedelta

default_args = {
    'owner': 'gayatri',
    'start_date': datetime.now() - timedelta(days=1),  # replaces days_ago(1)
    'retries': 1,
}

with DAG(
    dag_id='faker_mysql_dag',
    default_args=default_args,
    schedule='* * * * *',  # runs every minute
    catchup=False,
) as dag:

    insert_mysql = BashOperator(
        task_id='insert_fake_mysql',
        bash_command='/root/.local/share/pipx/venvs/apache-airflow/bin/python /root/weather_pipeline_project/faker/insert_fake_mysql.py',
    )

