from confluent_kafka import Producer
import json
import csv
import os 
import time

bootstrap_servers = 'localhost:9090'
topic = 'stock_topic'

conf = {'bootstrap.servers': bootstrap_servers}
producer = Producer(conf)
                
def produce_data():
    file_path = os.path.join("data", "data_car_prices_2.csv")
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile,fieldnames=['year','make','model','trim','body','transmission','state','condition','odometer','color','interior','seller','mmr'])
        for stock_data in reader:
            producer.produce(topic, key='1', value = json.dumps(stock_data))
            print(f'Produced: {stock_data}')
            producer.flush()
            time.sleep(1)

if __name__ == '__main__':
    produce_data()
