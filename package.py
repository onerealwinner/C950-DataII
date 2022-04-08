import json
from HashMap import HashData
from address import Addresses
from addressdistance import AddressDistances
from truck import Truck
import datetime
from datetime import timedelta

class PackageDelivery:
    """
        Maps to the data in packagedata.json
        The data contains all packages to deliver
    """

    def __init__(self):
        """
            Initalize my packages data and information about packages
        """
        
        #Create trucks and load them into the Trucks list
        self.Trucks = (Truck(1), Truck(2), Truck(3))

        #load package addresses
        self.Addresses = Addresses()

        #load package distances - initalize with the number of addresses
        self.AddressDistances = AddressDistances(self.Addresses.MyAddresses.size+1)

        #get Json from file
        with open('AppData/PackageData.json') as myFile:
            packageData = json.load(myFile)

        #create a hashtable with the rows
        self.MyPackages = HashData(len(packageData["Packages"]))

        #Big O ->O(n^2) - function loop in self.Addresses.getIdByStreetAddressAndZip
        for package in packageData['Packages']:
            myAddress = self.Addresses.getAddressByStreetAndZip(streetAddress=package["Address"],zip=package["Zip"]) #12
            package.update({"AddressId":myAddress["AddressId"]})

            #update some information about the package for the application
            status = "At Hub" if package["ArrivalTime"] == "08:00 AM" else "Not Arrived" #10 - valid status Not Arrived, At Hub, In Truck, Delivered
            package.update({"Status":status})
            package.update({"DeliveredTime":"5:00 PM"})
            package.update({"Id":package['PackageId']})
            package.update({"OnTruck":"0"})
            package.update({"LoadedOnTruckTime":""})
            package.update({"OnTime":"0"})
            package.update({"IsEarly":"0"})
            
            item = package
            self.MyPackages.insert(package['PackageId'], item)
    

    def deliverPackages(self, truckId):
        """
            Deliever all the packages in a truck
            Nearest Neighbor Algorithm
        """
        thisTruck = self.Trucks[truckId-1]

        #define output criteria from the loop 
        minDistance = 1000
        nextDestination = 0
        packageToDeliver = None
        
        #Nearest Neighbor Algorithm 
        #Loop through the packages in the truck and identify it's distance to the trucks current location
        #Big O -> O(n^2) - possible loop inside the hash table for truck addresses
        for p in thisTruck.Packages:
            #find the distance to this delivery address
            distanceToAddress = self.getDistanceOfTruckToAddress(thisTruck, p["AddressId"])

            #if this distance is less than the last distance - make this my new nearest neighbor and check the rest of the packages
            if distanceToAddress < minDistance:
                packageToDeliver = p
                minDistance = distanceToAddress
                nextDestination = p["AddressId"]

        #move the truck and delivery the package
        self.deliverPackage(thisTruck,nextDestination,minDistance,packageToDeliver)

        #if truck is out of packages, return this to home
        if len(thisTruck.Packages) > 0:
            self.deliverPackages(truckId) #delivery next package
        else:
            distanceToHub = self.getDistanceOfTruckToAddress(thisTruck, 0)
            self.deliverPackage(thisTruck, 0,distanceToHub, None)
    #end deliverPackages

    def deliverPackage(self, thisTruck, newAddress, distance, myPackage):
        """
            Update statuses to deliver a package
            Update Trucks current location
            This is a lot lines of code to just update and set values
            **** If myPackage = None - returning truck to home
        """
    
        seconds = ((distance / thisTruck.TruckSpeed) * 3600) 
        deliverTime = thisTruck.CurrentTime + datetime.timedelta(seconds=seconds)

        #setup status variables for package data
        willBeOnTime = True
        isEarly = False
        packageId = 0 
        if myPackage is not None:
            deliveryTime = datetime.datetime.strptime(myPackage["DeliveryDeadline"], '%H:%M')
            arrivalTime = datetime.datetime.strptime(myPackage["ArrivalTime"], '%H:%M')
            willBeOnTime = True if deliverTime.time() < deliveryTime.time() else False
            isEarly = True if deliverTime.time() > arrivalTime.time() else False
            packageId = myPackage["PackageId"]

        #create a travel path object to save in the truck route data
        travelPath = { \
            "PackageId" : packageId, \
            "WillBeOnTime" : willBeOnTime, \
            "IsEarly" : isEarly, \
            "FromId" : str(thisTruck.CurrentAddressId), \
            "ToId" : str(newAddress), \
            "StartTime" : thisTruck.CurrentTime.strftime("%H:%M:%S"), \
            "EndTime" : deliverTime.strftime("%H:%M:%S"), \
            "TravelTimeSeconds" : seconds, \
            "Distance" : str(distance), \
            "Order" : len(thisTruck.TravelPath)+1
        }

        #Update the truck information
        thisTruck.CurrentAddressId = newAddress
        thisTruck.DistanceTraveled += distance
        thisTruck.SecondsTraveled += seconds
        thisTruck.CurrentTime = deliverTime
                
        if distance > 0:
            thisTruck.Visits += 1
        
        thisTruck.TravelPath.append(travelPath)
        
        #remove Package from truck and update status 
        if myPackage is not None:
            thisTruck.Packages.remove(myPackage)
            myPackage["Status"] = "delivered"
            myPackage["OnTime"] = travelPath["WillBeOnTime"]
            myPackage["IsEarly"] = travelPath["IsEarly"]
            myPackage["OnTruck"] = str(thisTruck.TruckId)
            myPackage["DeliveredTime"] = thisTruck.CurrentTime.strftime("%m/%d/%Y %H:%M:%S")
            self.MyPackages.insert(myPackage["PackageId"], myPackage)
    #end deliverPackage 

    def getDistanceOfTruckToAddress(self, thisTruck, newAddress):
        """
            returns the distance of the truck to an address
        """
        distance = self.AddressDistances.getDistance(thisTruck.CurrentAddressId, newAddress)
        return float(distance["Distance"])


    def loadTruck(self, truckId, packageIds):
        """
            Load the truck with the packages to deliver
        """
        thisTruck = self.Trucks[truckId-1]
        thisTruck.PackageIds = packageIds
        thisTruck.PackageCount = len(packageIds)

        #Loop through list of ids and get a package on to the truck
        #Big O->O(n)
        for pId in packageIds:
            package = self.MyPackages.get(pId)

            #update package status
            package["Status"] = "On Truck"
            package["OnTruck"] = str(truckId)
            package["LoadedOnTruckTime"] = thisTruck.StartTime.strftime("%m/%d/%Y %H:%M:%S")
            self.MyPackages.insert(package["PackageId"], package)

            #add packaget to truck
            thisTruck.Packages.append(package)
    #end loadTruck

    def getPackageStatusAtTime(self, timeEntry, myPackage):
        #Start with the status of not arrived
        statusMsg = " had not arrived at hub"
        
        #get times at different points
        deliveredTime = datetime.datetime.strptime(myPackage["DeliveredTime"], '%m/%d/%Y %H:%M:%S')
        loadedTime = datetime.datetime.strptime(myPackage["LoadedOnTruckTime"], '%m/%d/%Y %H:%M:%S')
        arrivedTime = datetime.datetime.strptime(myPackage["ArrivalTime"], '%H:%M')

        #find the approaprite status for the input time
        if timeEntry.time() > deliveredTime.time():
            wasOnTime = " on time " if myPackage["OnTime"] == True else " late "
            statusMsg = " was delivered" + wasOnTime + "on truck " + str(myPackage["OnTruck"]) + " at " + \
                datetime.datetime.strptime(myPackage["DeliveredTime"], '%m/%d/%Y %H:%M:%S').strftime("%H:%M:%S") + \
                " deadline was " + myPackage["DeliveryDeadline"]
        elif timeEntry.time() > loadedTime.time() and timeEntry.time() < deliveredTime.time() :
            statusMsg = " was en route on truck " + str(myPackage["OnTruck"])
        elif timeEntry.time() > arrivedTime.time() and timeEntry.time() < loadedTime.time() :
            statusMsg = " was at hub" 

        return statusMsg
