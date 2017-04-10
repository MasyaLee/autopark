import threading
from random import randint
from time import sleep
from constants import Constants as Cons
from define_components import DefineComponents
from engine import Engine


class Car(Engine, threading.Thread):
    all_cars = []
    __tachograph = Cons.TACHOGRAPH_INITIAL_COUNT

    def __init__(self):
        super(Car, self).__init__()
        threading.Thread.__init__(self)
        self.tank_volume = DefineComponents.define_tank_volume(len(Car.all_cars))
        self.price = Cons.INITIAL_CARS_PRICE
        self.mileage = Cons.INITIAL_CARS_MILEAGE
        self.money_for_fuel = Cons.INITIAL_MONEY_FOR_FUEL
        self.money_spending = Cons.INITIAL_MONEY_SPENDING
        self.overhaul_count = Cons.INITIAL_OVERHAUL_COUNT
        self.refill_count = Cons.INITIAL_REFILL_COUNT
        self.amount_of_segments = Cons.AMOUNT_OF_SEGMENTS
        self.segment_1000 = Cons.SEGMENT_1000
        self.distance_for_consumption = Cons.DISTANCE_FOR_CONSUMPTION
        self.length_before_util = Cons.INITIAL_LENGTH_BEFORE_UTIL
        self.utilization = Cons.MILEAGE_TO_UTILIZATION
        self.route_length = (randint(Cons.INITIAL_LENGTH, Cons.FINAL_LENGTH))
        self.increasing_percent = Cons.INCREASING_PERCENT_OF_CONSUMPTION
        Car.all_cars.append(self)

    def drive(self):
        if self.mileage <= self.utilization:
            self.mileage += self.route_length
            Car.__tachograph = self.mileage
            self.length_before_util = self.utilization - self.mileage
            self.overhaul_count = self.route_length / self.max_mileage
            # self.fuel_consumption returns float
            self.refill_count = int(self.route_length / ((self.tank_volume / self.fuel_consumption) *
                                                         self.distance_for_consumption))
            '''Extra condition: fill Petrol cars with Ai92 (costs 2,2$/L) before they drive first 50.000 km,
            then fill them with Ai95(standard 2,4$/L)'''
            if self.engine == Cons.ENGINE_TYPE_PETROL:
                if self.mileage < Cons.CONDITION_OF_CHANGING_FUEL:
                    Engine.fuel_price = Cons.COST_OF_PETROL_Ai92
                else:
                    Engine.fuel_price = Cons.COST_OF_PETROL_Ai95
            self.money_for_fuel = self.refill_count * self.fuel_price
            self.money_spending = self.overhaul_count * self.price_overhaul + self.money_for_fuel
            self.amount_of_segments = self.route_length // self.segment_1000
            '''Every 1000 km of mileage reduces the price of a petrol car by 9,5$, a diesel car - by 10,5$,
            and increases fuel consumption by 1%'''
            for _ in range(0, self.amount_of_segments):
                self.fuel_consumption += self.increasing_percent * self.fuel_consumption
                self.price -= self.price_reduction
            for _ in range(0, self.refill_count):
                Car.filling_station()
        else:
            self.mileage = self.utilization

    @staticmethod
    def filling_station():
        sleep(Cons.TIME_OF_SLEEP)

    def info(self):
        if self.mileage < self.utilization:
            print('Mileage ' + str(self.mileage) + ' km')
            print('Residual price of the car is %s $' % self.price)
            print('Spent money for fuel {} $'.format(self.money_for_fuel))
            if not self.refill_count:
                print('Has not been refilled')
            else:
                print('%s times refilled' % self.refill_count)
            print('{} km until utilization'.format(self.length_before_util))
        else:
            print('The car is broken')
            print('Mileage is exceeded {}'.format(self.utilization))

    def run(self):
        semaphore.acquire()
        self.drive()
        self.info()
        semaphore.release()

        print(threading.active_count() - 1)
        print('-' * 80)


def create_cars(start_count=1, last_count=101):
    all_cars = [Car() for _ in range(start_count, last_count)]
    return all_cars


if __name__ == '__main__':
    semaphore = threading.BoundedSemaphore(10)
    my_cars = create_cars()
    for _ in my_cars:
        _.start()
