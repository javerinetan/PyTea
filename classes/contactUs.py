import random
import uuid
from datetime import datetime, date
# feedback_dict ={}
# feedback_id = str(random.randint(1000,9999))
# if feedback_id in feedback_dict:
#     feedback_id = str(random.randint(1000,9999))

class contactUs:
    # count_id = 0
    # feedback_dict = {}
    def __init__(self, first_name,last_name, email, saluation,feedback):
        self.__user_id = None
        self.__first_name = first_name
        self.__last_name = last_name
        self.__salutation = saluation
        self.__email = email
        self.__feedback = feedback
        self.__status = "Open"  # Add a default status of "open"
        self.__time = None

    def get_status(self):
        return self.__status

    def set_time(self, time):
        self.__time = time

    def get_time(self):
        return self.__time

    def set_status(self, status):
        self.__status = status

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self,last_name):
        self.__last_name = last_name

    def set_saluation(self, saluation):
        self.__salutation = saluation

    def set_email(self, email):
        self.__email = email

    def set_feedback(self,feedback):
        self.__feedback = feedback

    def set_user_id(self,id):
        self.__user_id=int(id)
    
    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_salutation(self):
        return self.__salutation

    def get_email(self):
        return self.__email
    def get_feedback(self):
        return self.__feedback

