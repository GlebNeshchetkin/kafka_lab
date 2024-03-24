import streamlit as st
import json
from confluent_kafka import Consumer, KafkaError
import pandas as pd
import sys

st.set_page_config(
    page_title="Real-Time Data Dashboard",
    layout='wide',
)

if 'makes_count' not in st.session_state:
    st.session_state['makes_count'] = {}
    
if 'bodies_count' not in st.session_state:
    st.session_state['bodies_count'] = {}
    
if 'sellers_count' not in st.session_state:
    st.session_state['sellers_count'] = {}
    
if 'predicted_prices' not in st.session_state:
    st.session_state['predicted_prices'] = []

bootstrap_servers = 'localhost:9090'
bootstrap_server_ml_results = 'localhost:9094'
topic = 'stock_topic'
topic_ml_results = 'ml_results_topic'

conf = {'bootstrap.servers': bootstrap_servers, 'group.id': 'my_consumers'}
consumer = Consumer(conf)
consumer.subscribe([topic])

conf_ml = {'bootstrap.servers': bootstrap_server_ml_results, 'group.id': 'my_consumers'}
consumer_ml_results = Consumer(conf_ml)
consumer_ml_results.subscribe([topic_ml_results])

st.title("Makers, Bodies and Sellers")

bodies_histogram_holder = st.empty()
makes_histogram_holder = st.empty()
sellers_histogram_holder = st.empty()

while True:
    msg = consumer.poll(100)

    if msg is not None:
        print("msg from consumer1")
        # print(msg)
        stock_data = json.loads(msg.value().decode('utf-8'))
        make = stock_data['make']
        body = stock_data['body']
        seller = stock_data['seller']
        # print(make,body,seller)
        
        if body != '':
            if body in st.session_state['bodies_count']:
                st.session_state['bodies_count'][body] += 1
            else:
                st.session_state['bodies_count'][body] = 1
        
        if make != '':
            if make in st.session_state['makes_count']:
                st.session_state['makes_count'][make] += 1
            else:
                st.session_state['makes_count'][make] = 1
                
        if seller != '':
            if seller in st.session_state['sellers_count']:
                st.session_state['sellers_count'][seller] += 1
            else:
                st.session_state['sellers_count'][seller] = 1
    
    
    # Create histogram for makes
    makes_histogram_holder.bar_chart(st.session_state['makes_count'])
    
    # Create histogram for bodies
    bodies_histogram_holder.bar_chart(st.session_state['bodies_count'])
    
    # Create histogram for sellers
    sellers_histogram_holder.bar_chart(st.session_state['sellers_count'])
    
    # predicted_prices_graph_holder.line_chart(st.session_state['predicted_prices'])