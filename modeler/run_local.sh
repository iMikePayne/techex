#!/bin/bash

echo -n "Choose a option create, run, stop, recreate, or delete: "
read VAR

create(){
  docker-compose --verbose up -d
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