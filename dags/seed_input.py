import shutil
from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'monitor_specific_file',
    default_args=default_args,
    schedule_interval=None,  # timedelta(minutes=10),
    is_paused_upon_creation=True
)

# Define the path of the file to monitor
file_path = "/data/stage/DEM_Challenge_Section1_DATASET.xlsx"

# Define the path of the directory to move the processed file
temp_file_path = "/data/temp/DEM_Challenge_Section1_DATASET.xlsx"

# Define the path of the directory to move the processed file
output_file_path = "/data/processed/DEM_Challenge_Section1_DATASET.xlsx"

# Setup postgres connection
pg_url = "postgresql://airflow:airflow@postgres:5432/airflow"
engine = create_engine(pg_url, echo=True)

# Create a sensor to monitor for the specific file
file_sensor = FileSensor(
    task_id='check_for_file',
    filepath=file_path,
    poke_interval=60,
    dag=dag
)


# Define the task to perform when the file is found
def found_file():
    shutil.move(file_path, temp_file_path)


def complete_file():
    shutil.move(temp_file_path, output_file_path)


def transform_data(data):
    # drop any rows with missing values
    data = data.dropna()

    # get full names
    data['full_name'] = data['first_name'] + ' ' + data['last_name']

    # convert email addresses to lowercase
    data['email'] = data['email'].str.lower()

    # extract IP address octets
    data['ip_octets'] = data['ip_address'].str.split('.').apply(lambda x: [int(octet) for octet in x])

    # calculate the sum of IP address octets
    data['ip_sum'] = data['ip_octets'].apply(lambda x: sum(x))

    # calculate the mean of IP address octets
    data['ip_mean'] = data['ip_octets'].apply(lambda x: sum(x) / len(x))

    # drop unnecessary columns
    data = data.drop(['ip_address', 'ip_octets'], axis=1)

    return data


# Define the task to perform when the file is found
def process_file():
    df = pd.read_excel(temp_file_path)
    df = transform_data(df)
    df.to_sql('person', engine, if_exists='replace')


def check_db():
    print('Check Insert')

    # print the DataFrame
    df2 = None
    with engine.begin() as conn:
        query = text("""SELECT * FROM person""")
        df2 = pd.read_sql_query(query, conn)

    print(df2)


# Create a task that depends on the file sensor and moves file to temp directory
temp_file_task = PythonOperator(
    task_id='temp_file',
    python_callable=found_file,
    dag=dag
)

# Create task to perform some action
process_file_task = PythonOperator(
    task_id='process_file',
    python_callable=process_file,
    dag=dag
)

# Create a task that depends on the file sensor and moves file from temp to processed directory
complete_file_task = PythonOperator(
    task_id='complete_file',
    python_callable=complete_file,
    dag=dag
)

# Create a task that depends on the file sensor and moves file from temp to processed directory
check_db_task = PythonOperator(
    task_id='check_db',
    python_callable=check_db,
    dag=dag
)
# Set the dependencies between the tasks
file_sensor >> temp_file_task >> process_file_task >> complete_file_task >> check_db_task
