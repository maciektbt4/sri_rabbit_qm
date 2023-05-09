import pika
import json


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('consumer_driver', exclusive=True)
queue_name = queue.method.queue

channel.queue_bind(
    exchange='bolid_alarm',
    queue = queue_name,
    routing_key ='driver'
)

def callback(ch, method, properties, body):
    payload = json.loads(body)   
    print ('-----------------')
    print ('Consumer 4: driver')    
    print ('Current bolid state:') 
    print (f'Date: {payload["date"]}')
    print (f'Alarm message: {payload["alarm_message"]}')
    print ('-----------------\n')
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(on_message_callback= callback, queue= queue_name)
print("Waiting for massges...")
channel.start_consuming()