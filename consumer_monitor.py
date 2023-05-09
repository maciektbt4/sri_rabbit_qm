import pika
import json
from classes.bolid import Bolid

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('consumer_monitor', exclusive=True)
queue_name = queue.method.queue

channel.queue_bind(
    exchange='bolid_state',
    queue = queue_name,
    routing_key ='bolid_state.report'
)

def callback(ch, method, properties, body):
    payload = json.loads(body) 
    bolid = Bolid(
        payload['engine_temperature'],
        payload['tire_pressure'],
        payload['oil_pressure'],
        payload['fuel_level'],
        payload['check_engine'],
    )
    bolid_warning = bolid.generate_warning()
    bolid_alarm = bolid.generate_alarm()

    print ('-----------------')
    print ('Consumer 2: monitor')
    print (f'Date: {payload["date"]}')

    if not bolid_warning and not bolid_alarm:
        print ("Everything's ok, keep going!")

    if bolid_warning:
        print ("Warning, one of parameter is outside range, inform mechanics!") 

    if bolid_alarm:
        print ("Alarm, serious demage, inform driver!") 
        
    print ('-----------------\n')
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(on_message_callback= callback, queue= queue_name)
print("Waiting for massges...")
channel.start_consuming()