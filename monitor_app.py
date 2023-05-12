from classes.consumers.monitor import Monitor

monitor = Monitor('consumer_monitor','bolid_state','bolid_state.report') # standard configuration when running with docker
# monitor = Monitor('consumer_monitor','bolid_state','bolid_state.report','localhost') # 'localhost' need to be used when running without docker 
monitor.start_consuming()