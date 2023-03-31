#!/bin/bash

echo -n "Choose a option create, run, stop, recreate, or delete: "
read VAR

dbHost="localhost"
dbName="airflow"
dbPort=5432
dbUser=airflow
dbPw=airflow

pg_url="postgresql://$dbUser:$dbPw@$dbHost:$dbPort/$dbName"
export PG_URL=$pg_url

create(){
  docker-compose up -d
  echo "Setting up airflow vars..."
  docker exec -it webserver scripts/set_airflow_vars.sh
#  python scripts/seed_db.py
}

run(){
  docker-compose start
}

stop(){
  docker-compose stop
}

delete(){
  docker-compose down --remove-orphans
  docker system prune -f
  docker system prune -a -f
  docker system prune --volumes -f
}

recreate(){
  stop
  delete
  create
}

if [[ $VAR = "create" ]]
then
  create
elif [[ $VAR = "run" ]]
then
  run
elif [[ $VAR = "stop" ]]
then
  stop
elif [[ $VAR = "delete" ]]
then
  delete
elif [[ $VAR = "recreate" ]]
then
  recreate
else
  echo "invalid options, please write or create or delete"
fi