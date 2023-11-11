from classes.user import User

class Staff(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password, 'staff')
        self.__leave=[]

# for leave information
    def get_leave(self):
        return self.__leave #returns the whole list with leave objects
    def set_leave(self, leave):
        self.__leave.append(leave)
    def clear_leave(self):
        self.__leave=[]

