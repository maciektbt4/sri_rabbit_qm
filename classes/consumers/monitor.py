# import pika
import json
from classes.bolid import Bolid
from classes.consumer import Consumer

class Monitor(Consumer):

    def __init__(self, queue_name, exchange_name, routing_key, host_name='rabbitmq', connection_attempts=10):
        super().__init__(queue_name, exchange_name, routing_key, host_name, connection_attempts)
        self.channel.exchange_declare(exchange='bolid_alarm', exchange_type='direct')

    def send_alert(self, channel, key, message):
        channel.basic_publish(exchange='bolid_alarm', routing_key=key, body=message)


    def callback(self, ch, method, properties, body):
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
            warning_message = 'Warning, at least one of parameter is outside range! Repair is needed.'
            body_warning['warning_message'] = warning_message
            print (f"{warning_message} Inform mechanics!") 
            self.send_alert(self.channel, 'mechanics', json.dumps(body_warning))

        if bolid_alarm:
            body_alarm = payload
            alarm_message = 'Alarm, serious demage! Prepare to stop on racetrack or return to pitstop !'
            body_alarm['alarm_message'] = alarm_message
            print (f"{alarm_message}, inform driver!") 
            self.send_alert(self.channel, 'driver', json.dumps(body_alarm))
            
        print ('-----------------\n')
        ch.basic_ack(delivery_tag = method.delivery_tag)
