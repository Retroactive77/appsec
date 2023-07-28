class redemptionHistory:
    def __init__(self):
        self.__itemName = None
        self.__itemQuantity = None
        self.__itemCost = None
        self.__redemptionDate = None
        self.__dAddress = None
        self.__redmeptionDateTime = None

    def set_itemName(self, itemName):
        self.__itemName = itemName

    def set_itemQuantity(self, itemQuantity):
        self.__itemQuantity = itemQuantity

    def set_itemCost(self, itemCost):
        self.__itemCost = itemCost

    def set_redemptionDate(self, redemptionDate):
        self.__redemptionDate = redemptionDate

    def set_dAddress(self, dAddress):
        self.__dAddress = dAddress

    def set_redemptionDateTime(self, redemptionDateTime):
        self.__redemptionDateTime = redemptionDateTime

    def get_itemName(self):
        return self.__itemName

    def get_itemQuantity(self):
        return self.__itemQuantity

    def get_itemCost(self):
        return self.__itemCost

    def get_redemptionDate(self):
        return self.__redemptionDate

    def get_dAddress(self):
        return self.__dAddress

    def get_redemptionDateTime(self):
        return self.__redemptionDateTime

    def to_dict(self):
        return {
            "itemName": self.__itemName,
            "itemQuantity": self.__itemQuantity,
            "itemCost": self.__itemCost,
            "redemptionDate": self.__redemptionDate,
            "dAddress": self.__dAddress,
            "redemptionDateTime": self.__redemptionDateTime
        }

    def from_dict(data):
        return redemptionHistory(data["itemName"], data["itemQuantity"], data["itemCost"], data["redemptionDate"], data["dAddress"], data["redemptionDatTime"])
