class StaffLeave:
    def __init__(self, start, end, type, reason):
        self.__leave_startdate= start
        self.__leave_enddate=end
        self.__leave_type=type
        self.__reason=reason

    def get_leave_startdate(self):
        return self.__leave_startdate
    def set_leave_startdate(self, date):
        self.__leave_startdate=date


    def get_leave_enddate(self):
        return self.__leave_enddate
    def set_leave_enddate(self, date):
        self.__leave_enddate=date 


    def get_leave_type(self):
        return self.__leave_type
    def set_leave_type(self, type):
        self.__leave_type=type

    def get_reason(self):
        return self.__reason
    def set_reason(self, reason):
        self.__reason=reason