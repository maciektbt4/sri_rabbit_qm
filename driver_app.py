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
        self.response = None
        self.correlation_id = '1'  # Unikalny identyfikator żądania
        
        self.result_channel.basic_publish(
            exchange='driver_supervisor',
            routing_key='driver_request',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id
            ),
            body = json.dumps(request)
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

class DriverThread(threading.Thread):

    def __init__(self, driver):
        super().__init__()
        self.daemon = True
        self.driver = driver
    
    def run(self):
        while(True):
            print('Send to supervisor: Do you agree go to pit stop (Y/N)?')
            response = self.driver.send_request('Do you agree go to pit stop (Y/N)?')
            print("Supervisor answered:", response)

# driver = Driver('consumer_driver','bolid_alarm','driver') # standard configuration when running with docker
driver = Driver(None,None,None,'localhost') # 'localhost' need to be used when running without docker 

driver_thread = DriverThread(driver)
driver_thread.start()

driver2 = Driver('consumer_driver','bolid_alarm','driver','localhost')
driver2.start_consuming()
