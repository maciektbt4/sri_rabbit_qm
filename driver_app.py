import json
from classes.consumer import Consumer


class Driver(Consumer):

    def __init__(self, queue_name, exchange_name, routing_key, host_name='rabbitmq', connection_attempts=10):
        super().__init__(queue_name,exchange_name, routing_key, host_name, connection_attempts)


    def callback(self, ch, method, properties, body):
        payload = json.loads(body)   
        print ('-----------------')
        print ('Consumer 4: driver')    
        print ('Current bolid state:') 
        print (f'Date: {payload["date"]}')
        print (f'Alarm message: {payload["alarm_message"]}')
        print ('-----------------\n')
        ch.basic_ack(delivery_tag = method.delivery_tag) 


# driver = Driver('consumer_driver','bolid_alarm','driver') # standard configuration when running with docker
driver = Driver('consumer_driver','bolid_alarm','driver','localhost') # 'localhost' need to be used when running without docker 
driver.start_consuming()