from classes.consumers.driver import Driver, DriverThread

# driver = Driver(None,None,None) # standard configuration when running with docker
driver = Driver(None,None,None,'localhost') # 'localhost' need to be used when running without docker 

driver_thread = DriverThread(driver)
driver_thread.start()

# driver2 = Driver('consumer_driver','bolid_alarm','driver') # standard configuration when running with docker
driver2 = Driver('consumer_driver','bolid_alarm','driver','localhost') # 'localhost' need to be used when running without docker 
driver2.start_consuming()
