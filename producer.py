import pika
import json


class Producer():
    
    def __init__(self, bolid, date):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='bolid_state',
            exchange_type='direct'
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
        print(f'{self.bolid_state["date"]}: Message: Bolid state sent')
        self.connection.close()
