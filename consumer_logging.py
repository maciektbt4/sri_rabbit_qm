import pika
import json


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('bolid_state_report')
queue_name = queue.method.queue

channel.queue_bind(
    exchange='bolid_state',
    queue = queue_name,
    routing_key ='bolid_state.report'
)

def callback(ch, method, properties, body):
    payload = json.loads(body)   
    print ('-----------------')
    print('Current bolid state:') 
    print (f'Date: {payload["date"]}')
    print (f'Engine temperature: {payload["engine_temperature"]}°')
    print (f'Tire pressure: {payload["tire_pressure"]} bar')
    print (f'Oil pressure: {payload["oil_pressure"]} PSI')
    print (f'Fuel level: {payload["fuel_level"]}%')
    print (f'Check engine: YES') if payload['check_engine'] else print (f'Check engine: NO')
    print ('-----------------\n')
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(on_message_callback= callback, queue= queue_name)
print("Waiting for massges...")
channel.start_consuming()