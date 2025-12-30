from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime , timedelta

default_args = {
    'owner': 'gayatri',
    'start_date': datetime.now() - timedelta(days=1),  # replaces days_ago(1),
    'retries': 1,
}

with DAG(
    dag_id='batch_etl_dag',
    default_args=default_args,
    schedule='@hourly',
    catchup=False,   # prevents backfilling old runs
) as dag:

    run_etl = BashOperator(
        task_id='run_batch_etl',
        bash_command='PYSPARK_PYTHON=/root/.local/share/pipx/venvs/apache-airflow/bin/python PYSPARK_DRIVER_PYTHON=/root/.local/share/pipx/venvs/apache-airflow/bin/python spark-submit --master local[*] /root/weather_pipeline_project/spark/batch_etl.py',
    )

