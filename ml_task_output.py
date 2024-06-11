import pika
import json

def callback(ch, method, properties, body):
        message = body.decode('utf-8')
        results = json.loads(message)
        print(f" [x] Recieved result from the queue: {results}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='ml_task_output', durable=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='ml_task', on_message_callback=callback)

        print(" [x] waiting for results. To exit press CTRL+C")
        channel.start_consuming()