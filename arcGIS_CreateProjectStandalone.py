import os, sys, arcpy
from arcgis.gis import GIS #ArcGIS API for Python
import getpass #Password hider
from tkinter import filedialog #Library for GUI
from tkinter import Tk #Library for GUI
import csv
root = Tk()
root.withdraw()

#Asking the user for connection info:
print("Welcome to the new project creator. Please, add the project manager, the group and the template Geodatabase!\n")
print("1. First, let's connect to your Portal.\n")
try:
    portalUrl = input("Portal URL: ")
    username = input("Username: ")
    pwd = getpass.getpass("Password: ")
    gis = GIS(portalUrl, username, pwd)
    print("SUCCESS: Connected to " + portalUrl + " as user " + username)
except:
    print("ERROR: Something didn't work here")
print("\n2. Create an account for the project manager.\n")
newUsername = input("Select new username: ")
newName = input("First name: ")
newLastName = input("Last name: ")
newEmail = input("Email: ")
newLevel = input("Level (1 or 2): ")
demo_user1 = gis.users.create(username= newUsername,
                             password='Renard123',
                             firstname = newName,
                             lastname = newLastName,
                             email= newEmail,
                             level = newLevel,
                             provider= 'arcgis')
gis.users.get(newUsername)
print("User " + newUsername +" created successfully!\n")
groupName = input("Enter the name of the group you want to place the user and the services: ")
myGroups= gis.groups.search('title:'+groupName)
if len(myGroups) == 0:
    print("Error: The group " + groupName + " does not exist!")
    createKey = input("Would you like to create a group called " + groupName + "? (y or n) ")
    if createKey == "y" or createKey == "Y":
        goodGroup = gis.groups.create(groupName,"python,toronto,uc")
    else:
        print("This wizard will end now")
        sys.exit()
else:
    goodGroup = myGroups[0]
try:
    goodGroup.add_users([newUsername])
    print("User " + newUsername + " added to group "+ goodGroup.title+" sucessfully\n")
except:
    print("Error adding the user " + newUsername + " to group " + goodGroup.title)
print("Now, let's create a copy of our template service for the new project\n")
nomProjet = input("Project Name: ")
descProjet = input("Project description: ")
tagsProjet = input("Tags (comma delimited)")
print("Please select the zipped geodatabase!")
gdbTemplate = filedialog.askopenfilename()
service_item = gis.content.add({'title':nomProjet,'description':descProjet,'tags':tagsProjet,'type':'File Geodatabase'},data= gdbTemplate,folder='packages')
publishedService = service_item.publish()
print("Service published successfully")
print("Adding service to the group " + goodGroup.title)
publishedService.share(groups=[goodGroup])
print("This Wizard will now close")