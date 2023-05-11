import pika
from pika.exceptions import AMQPConnectionError
import json
import datetime
import threading
import time


class Producer():
    
    def __init__(self, bolid, date, host_name='rabbitmq', connection_attempts=10):
        
        self.host_name = host_name
        self.connection_attempts = connection_attempts
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_name, connection_attempts=self.connection_attempts))
        
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='bolid_state',
            exchange_type='fanout'
        )
        self.bolid = bolid
        self.date = date
        self.bolid_state = {
            'date': str(self.date),
            'engine_temperature': bolid.engine_temperature,   
            'tire_pressure': bolid.tire_pressure,
            'oil_pressure': bolid.oil_pressure,
            'fuel_level': bolid.fuel_level,
            'check_engine': bolid.check_engine,
        }

    def publish_state(self):
        self.channel.basic_publish(
            exchange='bolid_state',
            routing_key='bolid_state.report',
            body = json.dumps(self.bolid_state)
        )

    def connection_close(self):
        self.connection.close()

    def actualize_date(self):
        self.date = Producer.current_time()
        self.bolid_state['date'] = Producer.current_time()

    def actualize_bolid_state(self, bolid):
        self.bolid = bolid
        self.bolid_state['engine_temperature'] = bolid.engine_temperature
        self.bolid_state['tire_pressure'] = bolid.tire_pressure
        self.bolid_state['oil_pressure'] = bolid.oil_pressure
        self.bolid_state['fuel_level'] = bolid.fuel_level
        self.bolid_state['check_engine'] = bolid.check_engine

    
    @staticmethod
    def current_time():
        dt = datetime.datetime.now()
        dt_without_ms = dt.strftime('%Y-%m-%d %H:%M:%S')  
        return dt_without_ms


class ProducerThread(threading.Thread):

    def __init__(self, producer):
        super().__init__()
        self.daemon = True
        self.producer = producer
    
    def run(self):
        while True:
            # Repeat code in 15s loop - sent notification every 15s
            self.producer.actualize_date()
            self.producer.publish_state()
            time.sleep(15)    