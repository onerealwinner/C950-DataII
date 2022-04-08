#Daniel Mudge 004124446
#--------------------------------------------------
# WGUUPS Truck Schedule
# Self-Adjusting Nearest Neighbor Algorithm used to plan truck routes of delivering packages
# The space-time complexity for this entire solution is O(n^2)
#
# Author: Daniel Mudge 004124446
# Last Mod: 5/15/2021
#--------------------------------------------------
import tkinter as tk
from tkinter import *
from datetime import *
from package import PackageDelivery

#Running the code from here, processes the data and brings up GUI with overview data
appStartTime = datetime.now() #check time to run the program

#Load Packages
packages = PackageDelivery()

##Instead of having the algorithm pick delivery packages I'm going to pick the packages
#Packages 13,14,15,16,19,20 must go on the same truck - I am using truck 1 for this
#Packages 3,18,36,38 must go on truck 2 
#Packages 6,28,28,32,9 cannot leave the hub before 9:05am
delivery1 = [1,4,13,14,15,16,19,20,21,29,30,31,32,34,39,40]
delivery2 = [3,5,6,18,25,26,36,37,38]
delivery3 = [2,7,8,9,10,11,12,17,22,23,24,27,28,33,35]

##TRUCK 1
#truck 1 goes at 8
startTime = datetime.now().replace(hour=8,minute=0,second=0, microsecond=0)
packages.Trucks[0].StartTime = startTime
packages.Trucks[0].CurrentTime = startTime

#load truck 1 and deliver the packages
packages.loadTruck(1, delivery1)
packages.deliverPackages(1)

##TRUCK 2
#truck 2 goes at 9:05
startTime = datetime.now().replace(hour=9,minute=5,second=0, microsecond=0)
packages.Trucks[1].StartTime = startTime
packages.Trucks[1].CurrentTime = startTime

#load truck 2 and deliver packages
packages.loadTruck(2, delivery2)
packages.deliverPackages(2)

##TRUCK 3
#truck 3 goes when truck 1 or truck 2 finishes
tempTime = packages.Trucks[0].CurrentTime
if packages.Trucks[1].CurrentTime.time() < packages.Trucks[0].CurrentTime.time():
    tempTime = packages.Trucks[1].CurrentTime

#Make sure Truck 3 until at least 10 20 (that is the latest package to deliver)
latestPackage = datetime.now().replace(hour=10,minute=20,second=0, microsecond=0)
if tempTime.time() < latestPackage.time():
    tempTime = latestPackage

packages.Trucks[2].StartTime = tempTime
packages.Trucks[2].CurrentTime = tempTime

#load the last truck and deliver the packages
packages.loadTruck(3, delivery3)
packages.deliverPackages(3)

appEndTime = datetime.now() #check time to run the program
runTime = appEndTime - appStartTime
print("This code was able to run in ", runTime.total_seconds() * 1000, "ms" )

#Check Data in console
def checkDataInConsole():
    """
        This method is can be called a developer to check the data in the terminal
    """
    print("Truck 1 Distance ", packages.Trucks[0].DistanceTraveled)
    print("Truck 1 Seconds ", packages.Trucks[0].SecondsTraveled)
    #print(packages.Trucks[0].TravelPath)
    print("Truck 2 Distance ", packages.Trucks[1].DistanceTraveled)
    print("Truck 2 Seconds ", packages.Trucks[1].SecondsTraveled)
    #print(packages.Trucks[1].TravelPath)
    print("Truck 3 Distance ", packages.Trucks[2].DistanceTraveled)
    print("Truck 3 Seconds ", packages.Trucks[2].SecondsTraveled)
    #print(packages.Trucks[2].TravelPath)
    print("Total Distance ", packages.Trucks[0].DistanceTraveled + packages.Trucks[1].DistanceTraveled + packages.Trucks[2].DistanceTraveled)
    print("Total Seconds ", packages.Trucks[0].SecondsTraveled + packages.Trucks[1].SecondsTraveled + packages.Trucks[2].SecondsTraveled)

checkDataInConsole()

###########################################
### Create a form to show the user data ###
### FORM Generation                     ###
###########################################

#create top level form
window = tk.Tk()
window.geometry("1680x980")

############
# packages Overview START
# list of packages and current status at the end deliveries
############

packageOverviewLabels = [] #holds the overlabels in a list

def createPackageOverviewLabels(curY):    
    """
        Creates the package overview labels for the form
    """
    #Loop through packages and create a new label to show overview information
    yOffset = curY + 18
    #O(n)
    for key, value in packages.MyPackages.items:
        newLabel = Label(window, text="")
        newLabel.place(x=startingX,y=yOffset)
        packageOverviewLabels.append(newLabel)
        yOffset += 18

def getPackageOverLabel(package, timeEntry):
    """
        the text to display for the package overview labels
    """
    if timeEntry is None:
        deliveredTime = datetime.strptime(package["DeliveredTime"], '%m/%d/%Y %H:%M:%S')
        return "Package " + str(package["PackageId"]) + " was " + \
            package["Status"] + " at " + deliveredTime.strftime("%H:%M") + \
            " to " + package["Address"] + " on truck " + package["OnTruck"] + \
            " delivery deadline was " + package["DeliveryDeadline"]
    else:
        return "Package " + str(package["PackageId"]) + packages.getPackageStatusAtTime(timeEntry,package)

def showPackageOverview(timeEntry):
    """
        Updates the package overview labels
    """
    labelIndex = 0
    #Loop through packages and create a new label to show overview information
    #O(n)
    for key, value in packages.MyPackages.items:
        p = packages.MyPackages.get(key)
        packageOverviewLabels[labelIndex].config(text=getPackageOverLabel(p,timeEntry))
        labelIndex+=1

def showPackageOverviewButton():
    """
        Event from user to re populate the package overview labels
    """
    inputText = packageOverviewTimeEntry.get()

    #clear text
    #Big O(n)
    for l in packageOverviewLabels:
        l.config(text="")

    if len(inputText) > 0:
        #validate a time was input correctly
        try:
            timeEntry = datetime.strptime(packageOverviewTimeEntry.get(), '%H:%M')
        except:
            packageOverviewLabels[0].config(text="Enter a time a in valid or leave blank for complete overview")
            return

        showPackageOverview(timeEntry)
    else:
        showPackageOverview(None)

#storing x, y here makes the components of this easy to move as a group
startingX = 320
startingY = 10

#Create a title label
packagesOverviewLabel = Label(window, text="Packages Overview:")
packagesOverviewLabel.place(x=startingX,y=startingY)

#Create Label to Show the entire distance
packagesOverviewLabel = Label(window, text="Total Driven Distance: " + str(packages.Trucks[0].DistanceTraveled + packages.Trucks[1].DistanceTraveled + packages.Trucks[2].DistanceTraveled))
packagesOverviewLabel.place(x=startingX,y=startingY+18)

#Create Label to Show the entire time (in seconds)
packagesOverviewLabel = Label(window, text="Total Driven Seconds: " + str(packages.Trucks[0].SecondsTraveled + packages.Trucks[1].SecondsTraveled + packages.Trucks[2].SecondsTraveled))
packagesOverviewLabel.place(x=startingX,y=startingY+36)

#Create Label to Show when the last truck got back to base
packagesOverviewLabel = Label(window, text="Last Truck Arrived: " + packages.Trucks[2].CurrentTime.strftime("%H:%M:%S") )
packagesOverviewLabel.place(x=startingX,y=startingY+54)

packageOverviewTimeEntry = Entry(window)
packageOverviewTimeEntry.place(x=startingX,y=startingY+78)

packageFormButton = Button(window, text="show overview at entered time (enter time HH:MM)", command=showPackageOverviewButton)
packageFormButton.place(x=startingX+100,y=startingY+78)

createPackageOverviewLabels(startingY+100)
showPackageOverview(None)

############
# packages Overview END
############

############
# Truck Info List START
# Show the packages each truck had route it took
############

def drawTruckData(startingX, startingY, truckId):
    """
        Draw form elements for a given truck 
    """
    #get the truck for these labels
    thisTruck = packages.Trucks[truckId-1]
    
    #title label
    truckLabel = Label(window, text="Truck " + str(truckId) + "\nPackages")
    truckLabel.place(x=startingX,y=startingY)

    #create a listbox for package id list
    truckList = Listbox(window, height=16, width=9)
    truckList.place(x=startingX,y=startingY+40)
    #O(n) 
    for key in thisTruck.PackageIds:
        truckList.insert(1,key)

    #route title label
    truckRoute = Label(window, text="Truck " + str(truckId) + "\nRoute")
    truckRoute.place(x=startingX+80,y=startingY)

    #Loop through travel path and create labels for each path
    index = 40
    #O(n)
    for item in thisTruck.TravelPath:
        packageText = "Package " + str(item["PackageId"]) + ": " if str(item["PackageId"]) != "0" else "Return from "
        newLabel = Label(window, text=packageText + item["FromId"] + " to " + item["ToId"] + " for " + item["Distance"] + " miles " \
            "Started At: " + item["StartTime"] + " Delivered At: " + item["EndTime"])
        newLabel.place(x=startingX+80,y=startingY+index)
        index += 18

    #Summary Information Title
    sumTitleLabel = Label(window, text="Truck " + str(truckId) + " Summary for its " + str(thisTruck.PackageCount)  + " packages:")
    sumTitleLabel.place(x=startingX+500,y=startingY+100)

    #Label for Distance Title
    distanceLabel = Label(window, text="Distance Traveled " + str(thisTruck.DistanceTraveled) + " miles")
    distanceLabel.place(x=startingX+500,y=startingY+130)

    #Label for Visits information
    visitsLabel = Label(window, text="Visited Addresses " + str(thisTruck.Visits))
    visitsLabel.place(x=startingX+500,y=startingY+150)

    #Label for time information
    timeLabel = Label(window, text="Time taken " + str(thisTruck.SecondsTraveled) + " seconds")
    timeLabel.place(x=startingX+500,y=startingY+170)

    #Label for route start and end information
    startTimeLabel = Label(window, text="Started Route At " + str(thisTruck.StartTime.strftime("%m/%d/%Y %H:%M:%S")))
    startTimeLabel.place(x=startingX+500,y=startingY+190)
    endedTimeLabel = Label(window, text="Ended Route At " + str(thisTruck.CurrentTime.strftime("%m/%d/%Y %H:%M:%S")))
    endedTimeLabel.place(x=startingX+500,y=startingY+210)

#truck 1
drawTruckData(950,10,1)
#truck 2
drawTruckData(950,360,2)
#truck 3 
drawTruckData(950,660,3)

############
# Truck Info List END
############

############
# Package Form START
# Allow a user to check a package status at a specific time
############

#function to show package at an inputed time
def showPackageAtTime():
    """
        Method to show package at an inputed time
    """
    packageResultsLabel.config(text="") #clear old results

    #validate packageId entry
    try:
        packageId = int(packageIdEntry.get())
        myPackage = packages.MyPackages.get(packageId)
    except:
        packageResultsLabel.config(text="Enter a valid package ID")
        return

    #validate a time was input correctly
    try:
        timeEntry = datetime.strptime(packageTimeEntry.get(), '%H:%M')
    except:
        packageResultsLabel.config(text="Enter a time a in valid format package ID")
        return

    #Update the label with the correct time
    packageResultsLabel.config(text="Package " + str(packageId) + \
        packages.getPackageStatusAtTime(timeEntry,myPackage))

#Package form input controls and labels
startingX = 20
startingY = 40

packageIdLabel = Label(window, text="Search for package at specific time")
packageIdLabel.place(x=startingX,y=startingY-20)

packageIdLabel = Label(window, text="Enter Package ID")
packageIdLabel.place(x=startingX,y=startingY)

packageIdEntry = Entry(window)
packageIdEntry.place(x=startingX,y=startingY+20)

packageTimeLabel = Label(window, text="Enter Time HH:MM (24hr)")
packageTimeLabel.place(x=startingX,y=startingY+40)

packageTimeEntry = Entry(window)
packageTimeEntry.place(x=startingX,y=startingY+60)

packageFormButton = Button(window, text="search", command=showPackageAtTime)
packageFormButton.place(x=startingX,y=startingY+80)

packageResultsLabel = Label(window, text="")
packageResultsLabel.place(x=startingX,y=startingY+110)

############
# Package Form END
# Allow a user to check a package status at a specific time
############

############
###########
##########
#########
########
#######
######
#####
####
###
##
#Start the form
window.mainloop()


