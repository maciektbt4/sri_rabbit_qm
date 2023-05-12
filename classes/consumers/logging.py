import json
from classes.consumer import Consumer


class Logging(Consumer):

    def __init__(self, queue_name, exchange_name, routing_key, host_name='rabbitmq', connection_attempts=10):
        super().__init__(queue_name, exchange_name, routing_key, host_name, connection_attempts)

    def callback(self, ch, method, properties, body):
        payload = json.loads(body)   
        print ('-----------------')
        print ('Consumer 1: logging')
        print ('Current bolid state:') 
        print (f'Date: {payload["date"]}')
        print (f'Engine temperature: {payload["engine_temperature"]}°C')
        print (f'Tire pressure: {payload["tire_pressure"]} bar')
        print (f'Oil pressure: {payload["oil_pressure"]} PSI')
        print (f'Fuel level: {payload["fuel_level"]}%')
        print (f'Check engine: YES') if payload['check_engine'] else print (f'Check engine: NO')
        print ('-----------------\n')
        ch.basic_ack(delivery_tag = method.delivery_tag)

