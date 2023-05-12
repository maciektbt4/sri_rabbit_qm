import pika
import json
from classes.consumer import Consumer


class Supervisor(Consumer):
    def __init__(self, queue_name, exchange_name, routing_key, host_name='rabbitmq', connection_attempts=10):
        super().__init__(queue_name, exchange_name, routing_key, host_name, connection_attempts)

    def callback(self, ch, method, properties, body):
        question = json.loads(body) 
        print ('-----------------')
        print ('Consumer 5: supervisor') 
        print (f'Driver question: {question}')
        user_input = input("Answer (Y/N): ").capitalize() 
        if user_input == "Y" or user_input == "YES":
            self.answer = 'yes'
        else:
            self.answer = 'no'
        self.publish_state()
        print ('-----------------\n')
    
    def publish_state(self):
        self.channel.basic_publish(
            exchange='driver_supervisor',
            routing_key='supervisor_response',
            body = json.dumps(self.answer)
        )

supervisor = Supervisor('','driver_supervisor','driver_request','localhost')
supervisor.start_consuming()