import pika
import json
from classes.bolid import Bolid

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', connection_attempts=10))
channel = connection.channel()

channel.exchange_declare(exchange='bolid_alarm', exchange_type='direct')

queue = channel.queue_declare('consumer_monitor', exclusive=True)
queue_name = queue.method.queue

channel.queue_bind(
    exchange='bolid_state',
    queue = queue_name,
    routing_key ='bolid_state.report'
)

def send_alert(channel, key, message):
    channel.basic_publish(exchange='bolid_alarm', routing_key=key, body=message)


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
        body_warning = payload
        warning_message = 'Warning, one of parameter is outside range! Repair is needed.'
        body_warning['warning_message'] = warning_message
        print (f"{warning_message} Inform mechanics!") 
        send_alert(channel, 'mechanics', json.dumps(body_warning))

    if bolid_alarm:
        body_alarm = payload
        alarm_message = 'Alarm, serious demage! Prepare to stop on racetrack or return to pitstop !'
        body_alarm['alarm_message'] = alarm_message
        print (f"{alarm_message}, inform driver!") 
        send_alert(channel, 'driver', json.dumps(body_alarm))
        
    print ('-----------------\n')
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(on_message_callback= callback, queue= queue_name)
print("Waiting for massages...")
channel.start_consuming()