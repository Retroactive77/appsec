import os

class redemptionProductInfo:
    def __init__(self):
        self.__redemptionProductName = None
        self.__redemptionProductCost = None
        self.__redemptionProductRetail = None
        self.__redemptionProductDescription = None

    def set_redemptionProductName(self, redemptionProductName):
        self.__redemptionProductName = redemptionProductName

    def set_redemptionProductCost(self, redemptionProductCost):
        self.__redemptionProductCost = redemptionProductCost

    def set_redemptionProductRetail(self, redemptionProductRetail):
        self.__redemptionProductRetail = redemptionProductRetail

    def set_redemptionProductDescription(self, redemptionProductDescription):
        self.__redemptionProductDescription = redemptionProductDescription

    def get_redemptionProductName(self):
        return self.__redemptionProductName

    def get_redemptionProductCost(self):
        return self.__redemptionProductCost

    def get_redemptionProductRetail(self):
        return self.__redemptionProductRetail

    def get_redemptionProductDescription(self):
        return self.__redemptionProductDescription


    def saveRedemptionProductImage(self, imageFile):
        existingImagePath = os.path.join("static", "images", "redemptionitem.png")

        if os.path.exists(existingImagePath):
            os.remove(existingImagePath)

        savePath = os.path.join("static", "images", "redemptionitem.png")

        with open(savePath, "wb") as file:
            file.write(imageFile.read())

        return savePath

    def to_dict(self):
        return {
            "redemptionProductName": self.__redemptionProductName,
            "redemptionProductCost": self.__redemptionProductCost,
            "redemptionProductRetail": self.__redemptionProductRetail,
            "redemptionProductDescription": self.__redemptionProductDescription,
        }

    def from_dict(data):
        return redemptionProductInfo(data["redemptionProductName"], data["redemptionProductCost"], data["redemptionProductRetail"], data["redemptionProductDescription"])




