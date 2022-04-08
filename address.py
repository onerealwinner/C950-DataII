from HashMap import HashData
import json

class Addresses:
    """
        Maps to the data in AddressData.json
        This is list of address packages will travel to
    """


    def __init__(self):
        """
            Initalize my address data
        """

        #data cleaning 5383 South East #104 = 5383 S East #104
        #get Json from file
        with open('AppData/AddressData.json') as myFile:
            addressData = json.load(myFile)

        #create new hashtable by the number of possibilities so each object will have a unique key
        self.MyAddresses = HashData(len(addressData["Addresses"]))

        #loop through my address data 
        #Big O -> O(n)
        for address in addressData['Addresses']:
            address.update({"Id":address['AddressId']})

            item = address
            self.MyAddresses.insert(address['AddressId'], item)


    def getAddressByStreetAndZip(self, streetAddress, zip):
        """
            Gets an address by a street address and zip code
            ID is index 0
            Can reduce by hashing the map by address or zip... hmmm        
        """

        #Loop through values in the hash table
        #Big O -> O(n) 
        for key, value in self.MyAddresses.items:
            address = value
            if(address['StreetAddress'] == streetAddress and address['ZipCode'] == zip):
                return address
