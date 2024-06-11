import pika
import json
import pandas as pd 


def send_ml_task(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='ml_task', durable=True)

    message = data.to_json(orient='split')
    channel.basic_publish(exchange='',
                          routing_key='ml_task',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))
    print(" [x] Sent ml task to the queue")
    connection.close()

data = pd.read_csv('spam.csv')
send_ml_task(data)