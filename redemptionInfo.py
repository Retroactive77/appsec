class redemptionInfo:
    def __init__(self):
        self.__quantity = None
        self.__dAddress = None
        self.__dpCode = None
        self.__otp = None

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_dAddress(self, dAddress):
        self.__dAddress = dAddress

    def set_dpCode(self, dpCode):
        self.__dpCode = dpCode

    def set_otp(self, otp):
        self.__otp = otp

    def get_quantity(self):
        return self.__quantity

    def get_dAddress(self):
        return self.__dAddress

    def get_dpCode(self):
        return self.__dpCode

    def get_otp(self):
        return self.__otp

    def to_dict(self):
        return {
            "quantity": self.__quantity,
            "dAddress": self.__dAddress,
            "dpCode": self.__dpCode,
            "otp": self.__otp
        }

    @staticmethod
    def from_dict(data):
        return redemptionInfo(data["quantity"], data["dAddress"], data["dpCode"], data["otp"])