from sklearn.naive_bayes import MultinomialNB
import pika
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

def callback(ch, method, properties, body):
        message = body.decode('utf-8')
        data = pd.read_json(message, orient='split')
        print(f" [x] recieved data from the queue")

        X = data['Category']
        y = data['Message']

        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
        
        feature = TfidfVectorizer(stop_words= 'english', lowercase=True)
        X_train_features = feature.fit_transform(X_train)
        X_test_features  = feature.transform(X_test)

        #y_train = y_train.astype('int')
        #y_test = y_test.astype('int')

        model = MultinomialNB()
        model.fit(X_train_features,y_train)

        testing_prediction = model.predict(X_test_features)
        testing_accuracy = accuracy_score(y_test, testing_prediction)
        print(f'Accuracy of this is: {testing_accuracy}')

        print(classification_report(y_test, testing_prediction))

        send_training_accuracy({'accuracy': testing_accuracy})

        ch.basic_ack(delivery_tag=method.delivery_tag)

def send_training_accuracy(result):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='ml_task_output', durable=True)

        message = json.dumps(result)
        channel.basic_publish(exchange='',
                          routing_key='ml_task_output',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))
        print(" [x] Sent ml task result to the queue")
        connection.close()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='ml_task', durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='ml_task', on_message_callback=callback)

print(' [*] Waiting for tasks. To exit press CTRL+C')
channel.start_consuming()