#HashMap Class
#special thanks to https://www.youtube.com/watch?v=9HFbhPscPU0
import json

class HashData:
    """
        Class model for the HashTable to store data from my json files
        This structure is going to store unique ID's as keys and retrieve information with that key
    """

    def __init__(self, size = 100):
        """
            Initalize the class to a specific number of buckets
        """
        self.size = size
        self.items = [None] * size


    def _get_hash(self, key):
        """
            Get the Hash Key
            The hash table is configured to have a unique bucket for all items
            rather than iterating through a list this hash table can efficiently get any item by it's id
        """
        return int(key-1)


    def insert(self, key, value) -> bool:
        """ 
            Adds an item to the hash data if it doesn't exist
        """
        hashKey = self._get_hash(key)
        hashKeyValue = [key, value]

        #check for adding or deleting
        if self.items[hashKey] is None:
            self.items[hashKey] = list(hashKeyValue)
            return True
        else:
            #check for an update hashKey
            counter = 0 #skip the first item which is just the key
            #Big O -> O(n)
            for hashKeyItem in self.items[hashKey]:
                if counter > 0:
                    jsonObj = hashKeyItem
                    if jsonObj["Id"] == key:
                        hashKeyItem[1] = value
                        return True
                counter += 1
            
            #if nothing was found add this item to the bucket
            self.items[hashKey].append(list(hashKeyValue))
            return True
    
    def get(self, key):
        """
            Return an object a specified key
            Each object is a JSON object
            So for example by getting package at a specific Id, this function will return all the package details included in the class model of package
        """
        retVal = None

        hashKey = self._get_hash(key)
        if self.items[hashKey] is not None:
            counter = 0 #skip the first item which is just the key
            #Big O -> O(n)
            for hashKeyItem in self.items[hashKey]:
                if counter > 0:
                    jsonObj = hashKeyItem
                    if jsonObj["Id"] == key:
                        retVal= hashKeyItem
                counter += 1
        return retVal
    
    def delete(self, key) -> bool:
        """
            Delete a value from the list
        """
        hashKey = self._get_hash(key)
        if self.items[hashKey] is None:
            return False #no item to delete
        
        #check bucket for key
        #Big O -> O(n)
        for i in range(0, len(self.map[hashKey])):
            if self.map[hashKey][i][0] == key:
                self.map[hashKey].pop(i)
                return True

    def print(self):
        """
            Print myself
        """
        print ("printing items")
        #Big O -> O(n)
        for obj in self.items:
            print(obj)