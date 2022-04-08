from datetime import *

class Truck:
    """
        Truck class model
    """

    def __init__(self, truckId):
        """
            Initiliaze the truck class
            Requires being assigned a TruckId 
        """
        self.TruckId = truckId
        self.TruckSpeed = 18 #speed in MPH
        self.Packages = [] #list of packages
        self.PackageIds = [] #List of packages truck can hold 16 packages
        self.PackageCount = 0
        self.Visits = 0
        self.DistanceTraveled = 0
        self.SecondsTraveled = 0
        self.TruckAddressId = 0
        self.CurrentAddressId = 0
        self.NextAddressId = 0
        self.TravelPath = [] #List to hold data of Truck Travelling Points
        self.StartTime = datetime.now()
        self.CurrentTime = datetime.now()