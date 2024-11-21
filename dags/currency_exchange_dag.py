import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.aws_s3_pipeline import upload_s3_pipeline
from pipelines.currency_exchange_pipeline import currency_exchange_pipeline

default_args = {
    'owner': 'Azeem',
    'start_date': datetime(2023, 10, 22)
}

file_postfix = datetime.now().strftime("%Y%m%d")

dag = DAG(
    dag_id='currency_exchange_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['currency', 'exchange','etl', 'pipeline']
)

# extraction from exchangeratesapi
extract = PythonOperator(
    task_id='currency_exchange_extraction',
    python_callable=currency_exchange_pipeline,
    op_kwargs={
        'file_name': f'currency_exchange_{file_postfix}',
        'subreddit': 'dataengineering',
        'time_filter': 'day',
        'limit': 100
    },
    dag=dag
)

# upload to s3
upload_s3 = PythonOperator(
    task_id='s3_upload',
    python_callable=upload_s3_pipeline,
    dag=dag
)

extract >> upload_s3
