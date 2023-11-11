class Drink:
    def __init__(self, name, quantity, size, sugar_level, cost):
        self.__drink_id = None
        self.__name = name
        self.__quantity = quantity
        self.__size = size
        self.__sugar_level = sugar_level
        self.__topping = []
        self.__cost = cost
        self.__total_cost= None

    def get_drink_id(self):
        return self.__drink_id

    def get_name(self):
        return self.__name

    def get_quantity(self):
        return self.__quantity

    def get_size(self):
        return self.__size

    def get_sugar_level(self):
        return self.__sugar_level

    def get_topping(self):
        return self.__topping

    def get_cost(self):
        return self.__cost
    def get_total_cost(self):
        self.__total_cost = round(float(self.__cost)*float(self.__quantity),2)
        return round(self.__total_cost, 2)

    def set_drink_id(self, drink_id):
        self.__drink_id = drink_id

    def set_name(self, name):
        self.__name = name

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_size(self, size):
        self.__size = size

    def set_sugar_level(self, sugar_level):
        self.__sugar_level = sugar_level
    def set_total_cost(self, cost):
        self.__total_cost = cost


    def set_topping(self, topping):
        if topping == "Classic Black Pearls":
            self.__cost += 0.60
        elif topping == "Signature Pearls":
            self.__cost += 0.60
        elif topping == "Jelly":
            self.__cost += 1.00
        self.__topping.append(topping)

    def reset_topping(self):
        for topping in self.__topping:
            if topping == "Classic Black Pearls":
                self.__cost -= 0.60
            elif topping == "Signature Pearls":
                self.__cost -= 0.60
            elif topping == "Jelly":
                self.__cost -= 1.00
        self.__topping=[]
