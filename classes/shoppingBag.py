from classes.drink import Drink
from datetime import datetime, date

class shoppingBag: 

    def __init__(self):
        self.__orders = {}
        self.__date = None
        self.__total_cost=None
        self.__user_email=None
        self.__order_id=None

    def add_order(self, drink_id, drink):
        self.__orders[drink_id] = drink

    def get_order(self):
        return self.__orders
    
    def delete_order(self, drink_id):
        self.__orders.pop(drink_id)

    def set_date(self, date):
        self.__date = date
    def get_date(self):
        return self.__date
    
    def get_total_cost(self):
        return self.__total_cost
    def set_total_cost(self, cost):
        self.__total_cost = cost

    def get_user_email(self):
        return self.__user_email
    def set_user_email(self, email):
        self.__user_email=email

    def get_order_id(self):
        return self.__order_id
    def set_order_id(self, order_id):
        self.__order_id=order_id



class ThaiMilkTea(Drink):
    def __init__(self, quantity, size, sugar_level):
        name = 'Thai Milk Tea'
        if size == 'Medium':
            cost = 4.90
        elif size == 'Large':
            cost = 5.90
        Drink.__init__(self, name, quantity, size, sugar_level, cost)


class BlackPearlTea(Drink):
    def __init__(self, quantity, size, sugar_level):
        name = 'Black Pearl Tea'
        if size == 'Medium':
            cost = 5.90
        elif size == 'Large':
            cost = 6.90
        Drink.__init__(self, name, quantity, size, sugar_level, cost)


class ThaiBubbleTea(Drink):
    def __init__(self, quantity, size, sugar_level):
        name = 'Thai Bubble Tea'
        if size == 'Medium':
            cost = 5.90
        elif size == 'Large':
            cost = 6.90
        Drink.__init__(self, name, quantity, size, sugar_level, cost)


