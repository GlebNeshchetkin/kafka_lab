from catboost import CatBoostRegressor
import streamlit as st
import json
from confluent_kafka import Consumer, Producer, KafkaError
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler

bootstrap_servers = 'localhost:9094'
topic_ml_results = 'ml_results_topic'

conf = {'bootstrap.servers': bootstrap_servers}
producer = Producer(conf)

model_path = os.path.join("model", "catboost_model.bin")
catboost_regressor = CatBoostRegressor()
catboost_regressor.load_model(model_path)

bootstrap_server2 = 'localhost:9098'
topic_proc = 'processed_data_topic'

conf = {'bootstrap.servers': bootstrap_server2, 'group.id': 'my_consumers'}
consumer = Consumer(conf)
consumer.subscribe([topic_proc])

while True:
    msg = consumer.poll(100)

    if msg is not None:
        data_received = json.loads(msg.value().decode('utf-8'))
        predicted_price = catboost_regressor.predict(data_received)
        # print(predicted_price)
        predicted_price = {'predicted_price': predicted_price[0]}
        producer.produce(topic_ml_results, key='1', value = json.dumps(predicted_price))
        # print(f'Produced: {predicted_price}')
        producer.flush()

