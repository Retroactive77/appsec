class allUsers:
    def __init__(self):
        self.__fName = None
        self.__lName = None
        self.__email = None
        self.__address = None
        self.__pcode = None

    def set_fName(self, fName):
        self.__fName = fName

    def set_lName(self, lName):
        self.__lName = lName

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_pcode(self, pcode):
        self.__pcode = pcode

    def get_fName(self):
        return self.__fName

    def get_lName(self):
        return self.__lName

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_pcode(self):
        return self.__pcode

    def to_dict(self):
        return {
            "fName": self.__fName,
            "lName": self.__lName,
            "email": self.__email,
            "address": self.__address,
            "pcode": self.__pcode
        }

    def from_dict(data):
        return allUsers(data["fName"], data["lName"], data["email"], data["address"], data["pcode"])