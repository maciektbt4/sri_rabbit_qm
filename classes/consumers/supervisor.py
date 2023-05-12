import pika
import json
from classes.consumer import Consumer


class Supervisor(Consumer):
    def __init__(self, queue_name, exchange_name, routing_key, host_name='rabbitmq', connection_attempts=10):
        super().__init__(queue_name, exchange_name, routing_key, host_name, connection_attempts)
        self.channel.exchange_declare(
            exchange='driver_supervisor',
            exchange_type='direct'
        )

    def callback(self, ch, method, properties, body):
        question = json.loads(body) 
        print ('-----------------')
        print ('Consumer 5: supervisor') 
        print (f'Date: {question["date"]}')
        print (f'Driver question: {question["text"]}')
        user_input = input("Answer (Y/N): ").capitalize() 
        if user_input == "Y" or user_input == "YES":
            self.answer = 'yes'
        else:
            self.answer = 'no'
        self.publish_state()
        print ('-----------------\n')
    
    def publish_state(self):
        self.message = {}
        self.message['date'] = Consumer.current_time()
        self.message['text'] = self.answer

        self.channel.basic_publish(
            exchange='driver_supervisor',
            routing_key='supervisor_response',
            body = json.dumps(self.message)
        )