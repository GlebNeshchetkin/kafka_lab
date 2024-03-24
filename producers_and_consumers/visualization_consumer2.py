import streamlit as st
import json
from confluent_kafka import Consumer, KafkaError
import pandas as pd
import sys

st.set_page_config(
    page_title="Real-Time Data Dashboard",
    layout='wide',
)

if 'predicted_prices' not in st.session_state:
    st.session_state['predicted_prices'] = []

bootstrap_server_ml_results = 'localhost:9094'
topic_ml_results = 'ml_results_topic'

conf_ml = {'bootstrap.servers': bootstrap_server_ml_results, 'group.id': 'my_consumers'}
consumer_ml_results = Consumer(conf_ml)
consumer_ml_results.subscribe([topic_ml_results])

st.title("Predicted prices")

predicted_prices_graph_holder = st.empty()

while True:
    msg_ml_res = consumer_ml_results.poll(1)

    if msg_ml_res is not None:
        # print("message_ml_prediction")
        message_with_price = json.loads(msg_ml_res.value().decode('utf-8'))
        predicted_price = message_with_price['predicted_price']
        st.session_state['predicted_prices'].append(predicted_price)
        # print(predicted_price)
    
    predicted_prices_graph_holder.line_chart(st.session_state['predicted_prices'])