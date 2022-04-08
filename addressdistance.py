import json
import HashMap
from HashMap import HashData

class AddressDistances:
    """
        Maps to the data in DistanceData.json
        This is list of distances between each point
    """


    def __init__(self, addressCount):
        """
            Initalize my address distance data
        """

        #get Json from file
        with open('AppData/DistanceData.json') as myFile:
            distanceData = json.load(myFile)

        #total number of address
        self.AddressCount = addressCount

        #create a hash with the - The key for this hash will be distanceId
        self.MyDistances = HashData(addressCount*addressCount)

        #Loop through data - create a distance id (update the data) and add it to the hashtable
        #Big O -> O(n)
        for distance in distanceData["Distances"]:
            distanceId = int(distance["AddressFrom"]) * addressCount + int(distance["AddressTo"])
            distance.update({"Id":distanceId})

            item = distance
            self.MyDistances.insert(distanceId, item)


    def getDistance(self, addressFrom, addressTo):
        """
            Gets a distance given an addressFrom and addressTo
        """

        #get a distanceId from the address from and to
        distanceId = int(addressFrom) * self.AddressCount + int(addressTo)

        #since the data goes both ways 0, 20 = 20, 0 - correct the Id to look at the right point if needed
        if addressFrom > addressTo:
            distanceId = int(addressTo) * self.AddressCount + int(addressFrom)

        return self.MyDistances.get(distanceId)
