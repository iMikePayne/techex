import shutil
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import json
import numpy as np

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'generate_test_case',
    default_args=default_args,
    schedule_interval=None,  # timedelta(minutes=10),
    is_paused_upon_creation=True
)


# Define the task to perform when the file is found
def generate_case():

    # Use a randomly generated dataset
    image_data = np.random.randint(1, 256, size=(1, 28, 28))

    image_pixel = image_data.tolist()

    input_data = json.dumps({'input_data': image_pixel})

    # Set up request headers
    headers = {'Content-Type': 'application/json'}

    # Send request to app.py
    response = requests.post('http://flask:7007/predict', headers=headers, data=input_data)

    # Parse the response
    if response.status_code == 200:
        output_data = json.loads(response.text)
        print(output_data)
    else:
        print('Error:', response.text)


run_test_case_task = PythonOperator(
    task_id='run_test_case',
    python_callable=generate_case,
    dag=dag
)

run_test_case_task