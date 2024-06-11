This is a repostory that shows how RabbitMQ can be used to create ML tasks. I
used one of my previous models(email classification model) and converted it to a rabbitMQ task where it sends the data csv file to the queue 
using the ```send_ml_task.py```.
Then the consumer receives the task ```receive_ml_task.py```.
The ```ml_task_output.py``` produces the output from the queue once the exchange is done .
