#!/bin/bash

# Run Docker Compose
cd ./docker_compose
docker-compose up -d

# Pause for 30 seconds
sleep 10

cd ../
# Run each Python file in the background with a pause of 10 seconds in between
python3 ./producers_and_consumers/main_producer1.py &
sleep 10

python3 ./producers_and_consumers/main_producer2.py &
sleep 10

python3 ./producers_and_consumers/data_processor_consumer.py &
sleep 10

python3 ./producers_and_consumers/ml_consumer.py &
sleep 10

streamlit run ./producers_and_consumers/visualization_consumer.py &
