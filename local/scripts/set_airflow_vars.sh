#!/bin/bash

airflow db init
airflow connections add postgres_conn --conn-type postgres --conn-host postgres --conn-login airflow --conn-password airflow --conn-schema airflow --conn-port 5432
