from classes.consumers.logging import Logging

# logging = Logging('bolid_state_report','bolid_state','bolid_state.report') # standard configuration when running with docker
logging = Logging('bolid_state_report','bolid_state','bolid_state.report','localhost') # 'localhost' need to be used when running without docker 
logging.start_consuming()