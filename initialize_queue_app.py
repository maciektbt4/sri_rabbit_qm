from classes.producer import Producer
from classes.bolid import Bolid
from classes.consumers.driver import Driver
from classes.consumers.logging import Logging
from classes.consumers.mechanics import Mechanics
from classes.consumers.monitor import Monitor
from classes.consumers.supervisor import Supervisor


def initialize_queue():

    is_hostname_localhost = True

    if is_hostname_localhost:
        # Create instances: bolid, producer and producer thread
        bolid  = Bolid(60.0, 1.1, 30.0, 100.0, False)

        # Create producer
        producer = Producer(bolid, Producer.current_time(),host_name='localhost') # 'localhost' need to be used when running without docker 

        # Create logging
        logging = Logging('bolid_state_report','bolid_state','bolid_state.report','localhost') # 'localhost' need to be used when running without docker 

        # Create monitor
        monitor = Monitor('consumer_monitor','bolid_state','bolid_state.report','localhost') # 'localhost' need to be used when running without docker 

        # Create mechanics
        mechanics = Mechanics('consumer_mechanics','bolid_alarm','mechanics','localhost') # 'localhost' need to be used when running without docker 

        # Create driver
        driver = Driver(None,None,None,'localhost') # 'localhost' need to be used when running without docker 
        driver2 = Driver('consumer_driver','bolid_alarm','driver','localhost') # 'localhost' need to be used when running without docker 

        # Create supervisor
        supervisor = Supervisor('','driver_supervisor','driver_request','localhost') # 'localhost' need to be used when running without docker 
    
    else:
         # Create instances: bolid, producer and producer thread
        bolid  = Bolid(60.0, 1.1, 30.0, 100.0, False)

        # Create producer
        producer = Producer(bolid, Producer.current_time()) # standard configuration when running with docker

        # Create logging
        logging = Logging('bolid_state_report','bolid_state','bolid_state.report') # standard configuration when running with docker

        # Create monitor
        monitor = Monitor('consumer_monitor','bolid_state','bolid_state.report') # standard configuration when running with docker

        # Create mechanics
        mechanics = Mechanics('consumer_mechanics','bolid_alarm','mechanics') # standard configuration when running with docker

        # Create driver
        driver = Driver(None,None,None) # standard configuration when running with docker
        driver2 = Driver('consumer_driver','bolid_alarm','driver') # standard configuration when running with docker

        # Create supervisor
        supervisor = Supervisor('','driver_supervisor','driver_request') # standard configuration when running with docker

    producer.connection_close()
    logging.connection_close()
    monitor.connection_close()
    mechanics.connection_close()
    driver.connection_close()
    driver2.connection_close()
    supervisor.connection_close()


initialize_queue()






