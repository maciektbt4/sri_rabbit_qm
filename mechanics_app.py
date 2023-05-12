from classes.consumers.mechanics import Mechanics

mechanics = Mechanics('consumer_mechanics','bolid_alarm','mechanics') # standard configuration when running with docker
# mechanics = Mechanics('consumer_mechanics','bolid_alarm','mechanics','localhost') # 'localhost' need to be used when running without docker 
mechanics.start_consuming()