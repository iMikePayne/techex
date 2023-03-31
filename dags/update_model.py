import shutil
from datetime import datetime, timedelta
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from datetime import datetime
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'update_ml_model',
    default_args=default_args,
    schedule_interval=None,#timedelta(minutes=5),
    is_paused_upon_creation=True
)

# get current date and time
current_datetime = datetime.now()
print("Current date & time : ", current_datetime)

# convert datetime obj to string
str_current_datetime = str(current_datetime)

# Define the path of the file to monitor
file_path = "/data/stage/model.h5"

# Define the path of the directory to move the processed file
temp_file_path = "/data/temp/model.h5"

# Define the path of the directory to move the processed file
output_file_path = "/data/processed/model.h5"
hidden_output_file_path = "/data/processed/.model.h5"

# Adding timestamp as sunset date for versioning
archive_file_path = "/data/archive/model_" + str_current_datetime + ".h5"

# Create a sensor to monitor for the specific file
file_sensor = FileSensor(
    task_id='check_for_model_file',
    filepath=file_path,
    poke_interval=60,
    dag=dag
)


def found_file():
    shutil.move(file_path, temp_file_path)


def update_file():
    # Archived and updated as a single task so the scheduler
    # doesn't create a situation where there is no current model
    # shutil.copy(output_file_path, hidden_output_file_path)
    try:
        shutil.move(output_file_path, archive_file_path)
    except IOError:
        # Initial load does not have an active model
        shutil.copy(temp_file_path, hidden_output_file_path)

    shutil.move(temp_file_path, output_file_path)


# Create a task that depends on the file sensor and moves file to temp directory
temp_file_task = PythonOperator(
    task_id='temp_model_file',
    python_callable=found_file,
    dag=dag
)

update_file_task = PythonOperator(
    task_id='update_model_file',
    python_callable=update_file,
    dag=dag
)

# Set the dependencies between the tasks
file_sensor >> temp_file_task >> update_file_task
