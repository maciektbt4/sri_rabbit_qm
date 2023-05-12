from classes.consumers.supervisor import Supervisor

supervisor = Supervisor('','driver_supervisor','driver_request') # standard configuration when running with docker
# supervisor = Supervisor('','driver_supervisor','driver_request','localhost') # 'localhost' need to be used when running without docker 
supervisor.start_consuming()