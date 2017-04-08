from constants import Constants as Cons


class DefineComponents(Cons, object):

    @staticmethod
    def define_engine_type(car_number):
        if (car_number + 1) % 3:
            return Cons.ENGINE_TYPE_PETROL
        else:
            return Cons.ENGINE_TYPE_DIESEL

    @staticmethod
    def define_tank_volume(car_number):
        if (car_number + 1) % 5:
            return Cons.TANK_1
        else:
            return Cons.TANK_2
