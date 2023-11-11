from datetime import datetime, date


class checkout:
    def __init__(self, address, postal_code, payment_method, card_name, card_number, card_expiration, card_cvv):
        self.__address = address
        self.__postal_code = postal_code
        self.__payment_method = payment_method
        self.__card_name = card_name
        self.__card_number = card_number
        self.__card_expiration = card_expiration
        self.__card_cvv = card_cvv

    def get_address(self):
        return self.__address

    def get_postal_code(self):
        return self.__postal_code
    
    def get_payment_method(self):
        return self.__payment_method
    
    def get_card_name(self):
        return self.__card_name

    def get_card_number(self):
        return self.__card_number
    
    def get_card_expiration(self):
        return self.__card_expiration

    def get_card_cvv(self):
        return self.__card_cvv

    def set_address(self, address):
        self.__address = address

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

    def set_payment_method(self, payment_method):
        self.__payment_method = payment_method

    def set_card_name(self, card_name):
        self.__card_name = card_name

    def set_card_number(self, card_number):
        self.__card_number = card_number

    def set_card_expiration(self, card_expiration):
        self.__card_expiration = card_expiration

    def set_card_cvv(self, card_cvv):
        self.__card_cvv = card_cvv


