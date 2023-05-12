from abc import ABC, abstractmethod
import pika
import datetime

class Consumer(ABC):

    def __init__(self, queue_name, exchange_name, routing_key, host_name='rabbitmq', connection_attempts=10):
        self.host_name = host_name
        self.connection_attempts = connection_attempts
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_name, connection_attempts=self.connection_attempts))
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue_name, exclusive=True)
        self.queue_name = self.queue.method.queue

        self.channel.queue_bind(
            exchange=exchange_name,
            queue = self.queue_name,
            routing_key =routing_key
        )


    @abstractmethod
    def callback(self):
        pass  

    def start_consuming(self):
        self.channel.basic_consume(on_message_callback= self.callback, queue= self.queue_name)
        print("Waiting for massages...")
        self.channel.start_consuming()

    def connection_close(self):
        self.connection.close()

    @staticmethod
    def current_time():
        dt = datetime.datetime.now()
        dt_without_ms = dt.strftime('%Y-%m-%d %H:%M:%S')  
        return dt_without_ms