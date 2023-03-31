# techex

## Prereq
- **Python 3.8+** installed
- **Pip3** installed and pointing to Python3 build
- **Docker Desktop** installed
    - Running `pip -V` should display a path to Python 3.8.14
- Dedicated **virtual env** for this repo:
    - Run `python3 -m venv ~/techex` to create the env
    - Add these line
      - `AIRFLOW_PROJ_DIR="{repo location}"`
      - `export AIRFLOW_PROJ_DIR`
    - Run `source ~/techex/bin/activate` to source your newly created env
    - Run `pip upgrade`
    - Run `pip install docker-compose`
    - Run `sudo chmod 666 /var/run/docker.sock` to ensure docker is runnable



## Running Local Airflow
**ALL DAGS ARE UNSCHEDULED TO CONSERVE SYSTEM RESOURCES**
1. Make sure **Docker Desktop** is running
2. Navigate to `techex/local` directory
3. Run `sh scripts/run_local.sh` and choose `create` to spin up airflow<br/>
4. After docker compose complete, airflow will take 3 minutes to initialize
5. If running locally, navigate to `http://localhost:8080`
6. Credentials
   - Username: `airflow`
   - Password: `airflow`
7. Postgres URL `postgresql://airflow:airflow@localhost:5432/airflow`


## Running Section 1

1. Place DEM_Challenge_Section1_DATASET.xlsx in `techex/data/stage`
2. Navigate to airflow and run *monitor_specific_file*
3. Results will be visible in `check_db` task in airflow UI

## Running Section 2

### Evaluating Base Model
**Endpoint** - `http://localhost:7007/predict`
1. Navigate to airflow and run *generate_test_case* (test cases are randomly generated)
2. Results will be visible in `run_test_case_task` task in airflow UI

### Generating New model

1. Make sure **Docker Desktop** is running
2. Navigate to `techex/modeler` directory
3. Update `training_iterations.txt` with number of iterations
4. Run `sh run_local.sh` and choose `create` to generate new model<br/>
5. Navigate to airflow and run *update_ml_model*
6. Archived models can be found in `techex/data/archive`
7. Navigate to airflow and run *generate_test_case* (test cases are randomly generated)
8. Results will be visible in `run_test_case_task` task in airflow UI

