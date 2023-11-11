from flask_login import UserMixin
class User():

    def __init__(self, name, email, password, user_type):
        self.__id=''
        self.__name=name
        self.__email=email
        self.__password=password
        self.__user_type = user_type

    def set_user_id(self,id):
        self.__id=str(id)
    # def get_user_id(self):
    #     self.__user_id

    def set_name(self,name):
        self.__name=name
    def get_name(self):
        return self.__name

    def set_email(self,email):
        self.__email=email
    def get_email(self):
        return self.__email

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password

    def get_user_type(self):
        return self.__user_type

    def set_user_type(self, type):
        self.__user_type = type

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.__id
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    # def __eq__(self, other):
    #     """
    #     Checks the equality of two `UserMixin` objects using `get_id`.
    #     """
    #     if isinstance(other, UserMixin):
    #         return self.get_id() == other.get_id()
    #     return NotImplemented

    def __ne__(self, other):
        """
        Checks the inequality of two `UserMixin` objects using `get_id`.
        """
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal