# -*- coding: utf-8 -*-
import threading
from random import randint
from Constants import *
from time import sleep


def define_engine_type(car_number):
    if (car_number + 1) % 3:
        return ENGINE_TYPE_PETROL
    else:
        return ENGINE_TYPE_DIESEL


def define_tank_volume(car_number):
    if (car_number + 1) % 5:
        return TANK_1
    else:
        return TANK_2


class Engine(object):
    def __init__(self):
        self.engine = define_engine_type(len(Car.all_cars))
        if self.engine == 'petrol':
            self.max_mileage = PETROL_MAX_MILEAGE
            self.fuel_consumption = PETROL_FUEL_CONSUMPTION
            self.fuel_price = COST_OF_PETROL_Ai92
            self.price_overhaul = PETROL_OVERHAUL
            self.price_reduction = CHEAP_RATE_FOR_PETROL_CAR
        else:
            self.max_mileage = DIESEL_MAX_MILEAGE
            self.fuel_consumption = DIESEL_FUEL_CONSUMPTION
            self.fuel_price = COST_OF_DIESEL
            self.price_overhaul = DIESEL_OVERHAUL
            self.price_reduction = CHEAP_RATE_FOR_DIESEL_CAR


class Car(Engine, threading.Thread):
    all_cars = []
    __tachograph = 0

    def __init__(self):
        Engine.__init__(self)
        threading.Thread.__init__(self)
        self.tank_volume = define_tank_volume(len(Car.all_cars))
        self.price = STARTING_CARS_PRICE
        self.mileage = STARTING_CARS_MILEAGE
        self.tank_total = self.tank_volume
        self.tank_current = self.tank_total
        self.money_for_fuel = MONEY_FOR_FUEL
        self.money_spent = MONEY_SPENT
        self.overhaul_count = 0
        self.refill_count = 0
        self.distance_1000_count = 0
        self.count_for_util = 0
        self.utilization = MILEAGE_TO_UTILIZATION
        self.route_length = (randint(0, 286000))        # int
        Car.all_cars.append(self)

    def drive(self):
        if self.mileage <= self.utilization:
            self.mileage += self.route_length
            Car.__tachograph = self.mileage
            self.count_for_util = self.utilization - Car.__tachograph
            self.overhaul_count = self.route_length / self.max_mileage   # кол-во капремонтов
            self.refill_count = int(self.route_length / ((self.tank_volume / self.fuel_consumption) * 100))
            if self.engine == ENGINE_TYPE_PETROL:           # extra condition
                if self.mileage < 50000:
                    Engine.fuel_price = COST_OF_PETROL_Ai92
                else:
                    Engine.fuel_price = COST_OF_PETROL_Ai95
            self.money_for_fuel = (self.refill_count * self.fuel_price)  # кол-во потраченных денег
            self.money_for_fuel = (self.refill_count * self.fuel_price)
            self.money_spent = int((self.overhaul_count * self.price_overhaul) + self.money_for_fuel)
            self.distance_1000_count = self.route_length // 1000
            for _ in range(0, self.distance_1000_count):
                self.fuel_consumption += 0.01 * self.fuel_consumption
                self.price -= self.price_reduction
            for _ in range(0, self.refill_count):
                Car.filling_station(self)
        else:
            self.mileage = self.utilization

    @staticmethod
    def filling_station(self):
        sleep(0.3)

    def info(self):
        if self.mileage < self.utilization:
            print('Mileage ' + str(self.mileage) + ' km')
            print('Residual price of the car is %s $' % self.price)         # остаточная стоимость
            print('Spent money for fuel {} $'.format(self.money_for_fuel))
            if self.refill_count == 0:
                print('Has not been refilled')
            else:
                print('%s times refilled' % self.refill_count)
            print('{} km until utilization'.format(self.count_for_util))
        else:
            print('The car is broken')
            print('Mileage is exceeded {}'.format(self.utilization))        # превышен пробег

    # def __repr__(self):
    #     return self.engine + ' : ' + str(self.price) + ' : ' + str(self.count_for_util)

    def run(self):
        semaphore.acquire()
        self.drive()
        self.info()
        semaphore.release()

        print(threading.active_count())
        print('-' * 80)


def create_cars(start_count=0, last_count=101):
    all_cars = [Car() for _ in range(start_count, last_count)]
    return all_cars


# class ThreadingDrive(threading.Thread, Car):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         Car.__init__(self)
#
#     def run(self):
#         Car.drive(self)
#         print('-' * 80)                            # p1 = ThreadingDrive()
#         Car.info(self)                             # p1.start()
#
#         print(threading.active_count())
if __name__ == '__main__':
    semaphore = threading.BoundedSemaphore(10)
    my_cars = create_cars()
    for _ in my_cars:
        _.start()

    # car = ThreadingDrive()
    # car.start()






