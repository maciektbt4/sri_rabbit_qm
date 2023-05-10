from producer import Producer, ProducerThread
from classes.bolid import Bolid

# Create instances: bolid, producer and producer thread
bolid  = Bolid(60.0, 1.1, 30.0, 100.0, False)
# Create producer
producer = Producer(bolid, Producer.current_time())
producer_thread = ProducerThread(producer)
producer_thread.start()


# Ease interface to change bolid data
while(True):
    user_input = input("Do you want to change bolid parameters? (Y/N): ").capitalize()    
    if user_input == "Y":
        # Take new bolid parameters from user
        new_engine_temperature = float(input("Actualize engine temperature (warning > 230°C; alarm > 276°C): "))
        new_tire_pressure = float(input("Actualize tire pressure (warning < 1.1 bar; alarm < 0.88 bar): "))
        new_oil_pressure = float(input("Actualize oil pressure (20 PSI > warning > 90 PSI; 16 PSI > alarm > 108 PSI): "))
        new_fuel_level = float(input("Actualize fuel level (warning < 5% bar; alarm  < 4%): "))
        new_check_engine = True if (input("Enginge is damaged ? (Y/N)").capitalize() == 'Y') else False 

        # Actualize bolid parameters
        bolid.engine_temperature = new_engine_temperature
        bolid.tire_pressure = new_tire_pressure
        bolid.oil_pressure = new_oil_pressure
        bolid.fuel_level = new_fuel_level
        bolid.check_engine = new_check_engine
        producer.actualize_bolid_state(bolid)

