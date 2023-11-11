from classes.user import User

class Customer(User):
    def __init__(self, name, email, birth_month, password):
        super().__init__(name, email, password, 'customer')
        self.__birth_month=birth_month
        self.__address= None
        self.__postal_code= None
        # self.__past_orders={} #store multiple past orders (shopping bag objects)
        self.__shopping_bag=None #only one shoppingbag object stored inside
        self.__points=0

    
    def get_birth_month(self):
        return self.__birth_month
    
    def set_birth_month(self, birth_month):
        self.__birth_month = birth_month

    def set_address(self,address):
        self.__address=str(address)
    def get_address(self):
        return self.__address

    def set_postal_code(self,code):
        self.__postal_code=str(code)
    def get_postal_code(self):
        return self.__postal_code

    # def get_past_orders(self):
    #     return self.__past_orders #returns the whole list with order objects
    # def set_past_order(self, id, order):
    #     self.__past_orders[id]=order
    # def delete_past_order(self, id):
    #     self.__past_orders.pop(id)
    # def edit_past_order(self, id, order):
    #     self.__past_orders[id]=order

    def set_shopping_bag(self, bag):
        self.__shopping_bag=bag
    def get_shopping_bag(self):
        return self.__shopping_bag
    def reset_shopping_bag(self):
        self.__shopping_bag=None

    def get_points(self):
        return self.__points
    def set_points(self, points):
        self.__points=points


