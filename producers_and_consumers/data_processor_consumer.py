import json
from confluent_kafka import Consumer, Producer, KafkaError
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle

categorical_cols = ['make', 'model', 'trim', 'body', 'transmission', 'state', 'color', 'interior', 'seller']

with open('./labels/label_encoders.pkl', 'rb') as file:
    label_encoders = pickle.load(file)
    
# print(label_encoders['condition'])
    
def preprocess_single_row(row, label_encoders):
    if row['year'].values[0].startswith("\ufeff"):
        row['year'].values[0] = row['year'].values[0][len("\ufeff"):]
    for col in categorical_cols:
        if col in row:
            value = row[col].values[0]
            if value in set(label_encoders[col].keys()):
                row[col] = label_encoders[col][value]
            else:
                row[col] = -1
    row = row.astype(int)
    return row


bootstrap_server2 = 'localhost:9098'
topic_proc = 'processed_data_topic'

bootstrap_servers = 'localhost:9090'
topic = 'stock_topic'

conf = {'bootstrap.servers': bootstrap_servers, 'group.id': 'my_consumers'}
consumer = Consumer(conf)
consumer.subscribe([topic])

conf_prod = {'bootstrap.servers': bootstrap_server2}
producer = Producer(conf_prod)

while True:
    msg = consumer.poll(1)
    if msg is not None:
        msg = msg.value()
        if msg is not None:
            data_received = json.loads(msg.decode('utf-8'))
            # print(data_received)
            if not "" in data_received.values():
                data_received = pd.DataFrame(data_received, index=[0])
                if not any((pd.isnull(x) or x=='') for x in data_received):
                    data_received = preprocess_single_row(data_received,label_encoders)
                    # print(type(data_received))
                    data_received = data_received.values.tolist()
                    print(data_received)
                    producer.produce(topic_proc, key='1', value = json.dumps(data_received))
                    producer.flush()

