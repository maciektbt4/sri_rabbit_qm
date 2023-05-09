class Bolid():
    MAX_ENGINE_TEMPERATURE = 230.0
    MIN_TIRE_PRESSURE = 0.7
    MAX_OIL_PRESSURE = 90.0
    MIN_OIL_PRESSURE = 20.0
    MIN_FUEL_LEVEL = 5.0
    MAX_ALARM_FACTOR = 1.2 # 20% over max range
    MIN_ALARM_FACTOR = 0.8 # 20% below min range


    def __init__(self, engine_temperature, tire_pressure, oil_pressure, fuel_level, check_engine):
        self.engine_temperature = engine_temperature
        self.tire_pressure = tire_pressure
        self.oil_pressure = oil_pressure
        self.fuel_level = fuel_level
        self.check_engine = check_engine

    def generate_warning(self):
        if self.engine_temperature > Bolid.MAX_ENGINE_TEMPERATURE or\
            self.tire_pressure < Bolid.MIN_TIRE_PRESSURE or\
            self.oil_pressure > Bolid.MAX_OIL_PRESSURE or self.oil_pressure < Bolid.MIN_OIL_PRESSURE or\
            self.MIN_FUEL_LEVEL < Bolid.MIN_FUEL_LEVEL or self.check_engine:
            return True
        return False
    
    def generate_alarm(self):
        if self.engine_temperature > Bolid.MAX_ENGINE_TEMPERATURE * Bolid.MAX_ALARM_FACTOR or\
            self.tire_pressure < Bolid.MIN_TIRE_PRESSURE * Bolid.MIN_ALARM_FACTOR or\
            self.oil_pressure > Bolid.MAX_OIL_PRESSURE * Bolid.MAX_ALARM_FACTOR or \
            self.oil_pressure < Bolid.MIN_OIL_PRESSURE * Bolid.MIN_ALARM_FACTOR or\
            self.MIN_FUEL_LEVEL < Bolid.MIN_FUEL_LEVEL * Bolid.MIN_ALARM_FACTOR or self.check_engine:
            return True
        return False    
