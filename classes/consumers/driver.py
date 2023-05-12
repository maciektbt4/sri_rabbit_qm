import json
import pika
from classes.consumer import Consumer
import threading



class Driver(Consumer):

    def __init__(self, queue_name, exchange_name, routing_key, host_name='rabbitmq', connection_attempts=10):
        
        if queue_name is None and exchange_name is None and routing_key is None:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_name, connection_attempts=connection_attempts))
        else:
            super().__init__(queue_name,exchange_name, routing_key, host_name, connection_attempts)      

        self.result_channel = self.connection.channel()
        self.result = self.result_channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = self.result.method.queue
        self.result_channel.exchange_declare(
            exchange='driver_supervisor',
            exchange_type='direct'
        )
        self.result_channel.queue_bind(
            exchange='driver_supervisor',
            queue = self.callback_queue,
            routing_key ='supervisor_response'
        )
        self.result_channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.result_channel.exchange_declare(
            exchange='driver_supervisor',
            exchange_type='direct'
        )

    def on_response(self, ch, method, props, body):
        # if props.correlation_id == self.correlation_id:
            self.response = body
    
    def send_request(self, request):
        self.message = {}
        self.message['date'] = Consumer.current_time()
        self.message['text'] = request

        self.response = None
        self.correlation_id = '1'  # Unikalny identyfikator żądania
        
        self.result_channel.basic_publish(
            exchange='driver_supervisor',
            routing_key='driver_request',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id
            ),
            body = json.dumps(self.message)
        )
        
        while self.response is None:
            self.connection.process_data_events()
        
        return self.response.decode()    

    def callback(self, ch, method, properties, body):
        payload = json.loads(body)   
        print ('-----------------')
        print ('Consumer 4: driver')    
        print ('Current bolid state:') 
        print (f'Date: {payload["date"]}')
        print (f'Alarm message: {payload["alarm_message"]}')
        print ('-----------------\n')
        ch.basic_ack(delivery_tag = method.delivery_tag) 
        self.print_supervisor_question()
    
    def print_supervisor_question(self):  
        print()
        print('Do you want to send following question to supervisor:')      
        print('"Do you agree go to pit stop (Y/N)?"')

class DriverThread(threading.Thread):

    def __init__(self, driver):
        super().__init__()
        self.daemon = True
        self.driver = driver
    
    def run(self):
        while(True):
            self.driver.print_supervisor_question()
            user_input = input().upper()
            if user_input == "Y" or user_input == "YES":                
                response = self.driver.send_request('Do you agree go to pit stop (Y/N)?')    
                print('-------------')            
                print("Supervisor answered:")
                answer = json.loads(response) 
                print (f'Date: {answer["date"]}')
                print (f'Driver question: {answer["text"]}')
                print('-------------')   
