from producer import Producer
from classes.bolid import Bolid
import datetime

bolid  = Bolid(60.0, 1.1, 30.0, 100, False)
dt = datetime.datetime.now()
dt_without_ms = dt.strftime('%Y-%m-%d %H:%M:%S')  

producer = Producer(bolid, dt_without_ms)
producer.publish_state()