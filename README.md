# Kafka Car Price Prediction Lab

This project focuses on predicting car prices using CatBoost regression. It leverages Kafka for message queuing and stream processing, dividing the system into producers and consumers.

## Structure

### Producers and Consumers

Producers and consumers are organized within the `\producers_and_consumers` folder.

- **Main Producers**: `main_producer1` and `main_producer2` are responsible for sending data for price prediction.

- **Data Processor Consumer**: `data_processor_consumer` receives raw data and preprocesses it for consumption by the machine learning model.

- **ML Consumer**: `ml_consumer` predicts car prices using a pretrained CatBoost regressor model.

- **Visualization Consumers**: `visualization_consumer` and `visualization_consumer2` utilize Streamlit to visualize data. The first consumer plots histograms for entered data, while the second one plots a line graph for predicted prices.

### Labels

The `labels` folder contains the labels dictionary for data preprocessing.

### Model

The `model` folder contains the pretrained CatBoost regression model file. Model training is documented in the Jupyter Notebook (`ipynb`) file in `model_training` folder.

### Data

Raw data files reside in the `data` folder. These files are read by `main_producer1` and `main_producer2` for processing.

### Docker-Compose

The configuration for Kafka using Docker Compose is available in the `docker_compose` folder.

## How to Run

### Ubuntu

Two scripts are provided for running the system:

- **run_file1.sh**: This script executes the system with the first visualization.

- **run_file2.sh**: Use this script for running the system with the second visualization.
