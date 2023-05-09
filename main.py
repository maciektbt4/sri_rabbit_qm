from producer import Producer
from classes.bolid import Bolid
import time

bolid  = Bolid(60.0, 1.1, 30.0, 100, False)
producer = Producer(bolid, Producer.current_time())

while(True):
    producer.actualize_date()
    producer.publish_state()
    time.sleep(15)
