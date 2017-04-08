from constants import Constants as Cons
from define_components import DefineComponents
from park import *


class Engine(Cons, object):
    def __init__(self):
        self.engine = DefineComponents.define_engine_type(len(Car.all_cars))
        if self.engine == 'petrol':
            self.max_mileage = Cons.PETROL_MAX_MILEAGE
            self.fuel_consumption = Cons.PETROL_FUEL_CONSUMPTION
            self.fuel_price = Cons.COST_OF_PETROL_Ai92
            self.price_overhaul = Cons.PETROL_OVERHAUL
            self.price_reduction = Cons.CHEAP_RATE_FOR_PETROL_CAR
        else:
            self.max_mileage = Cons.DIESEL_MAX_MILEAGE
            self.fuel_consumption = Cons.DIESEL_FUEL_CONSUMPTION
            self.fuel_price = Cons.COST_OF_DIESEL
            self.price_overhaul = Cons.DIESEL_OVERHAUL
            self.price_reduction = Cons.CHEAP_RATE_FOR_DIESEL_CAR
