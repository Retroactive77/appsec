class viewPoints:
    def __init__(self):
        self.__points = 0
        self.__expiryDate = "noDate"

    def set_points(self, points):
        self.__points = points

    def set_expiryDate(self, expiryDate):
        self.__expiryDate = expiryDate

    def get_points(self):
        return self.__points

    def get_expiryDate(self):
        return self.__expiryDate

    def to_dict(self):
        return {
            "points": self.__points,
            "expiryDate": self.__expiryDate,
        }

    def from_dict(data):
        return viewPoints(data["points"], data["expiryDate"])
