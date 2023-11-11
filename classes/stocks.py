class Inventory():
    def __init__(self):
        self.__bubble=20
        self.__milk=20
        self.__cup=20
        self.__tea=20
        self.__signature_pearls=20
        self.__jelly=20


    def restock_bubble(self, value):
        self.__bubble=int(value)
    def restock_milk(self, value):
        self.__milk=int(value)
    def restock_cup(self, value):
        self.__cup=int(value)
    def restock_tea(self, value):
        self.__tea=int(value)
    def restock_signature_pearls(self, value):
        self.__signature_pearls=int(value)
    def restock_jelly(self, value):
        self.__jelly=int(value)


    def used_bubble(self):
        self.__bubble-=1
    def used_milk(self):
        self.__milk-=1
    def used_cup(self):
        self.__cup-=1
    def used_tea(self):
        self.__tea-=1
    def used_signature_pearls(self):
        self.__signature_pearls-=1
    def used_jelly(self):
        self.__jelly-=1


    def get_bubble(self):
        return self.__bubble
    def get_milk(self):
        return self.__milk
    def get_cup(self):
        return self.__cup
    def get_tea(self):
        return self.__tea
    def get_signature_pearls(self):
        return self.__signature_pearls
    def get_jelly(self):
        return self.__jelly
    