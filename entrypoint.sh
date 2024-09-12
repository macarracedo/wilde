#!/bin/bash
export PYTHONPATH=src
echo "The recieved connection string is $DB_CONNECTION_STRING"
echo "Starting the flask server"
touch log_file.txt
python src/wilde/rest/app.py $DB_CONNECTION_STRING