import os, sys, arcpy
from arcgis.gis import GIS #ArcGIS API for Python


#Hardcoded user info:
portalUrl = r"yourorgaccount.maps.arcgis.com"
username = "yourusername"
pwd = "yourpassword"
#Connection to the GIS
try:
    gis = GIS(portalUrl, username, pwd)
    arcpy.AddMessage("SUCCESS: Connected to " + portalUrl + " as user " + username)
except:
    arcpy.AddMessage("ERROR: Something didn't work here")
    
#Creating the account for the project manager with the variables provided by the user.    
arcpy.AddMessage("\n2. Creating an account for the project manager.\n")
newUsername = arcpy.GetParameterAsText(0)
newName = arcpy.GetParameterAsText(1)
newLastName = arcpy.GetParameterAsText(2)
newEmail = arcpy.GetParameterAsText(3)
newLevel = arcpy.GetParameterAsText(4)
demo_user1 = gis.users.create(username= newUsername,
                             password='Renard123',
                             firstname = newName,
                             lastname = newLastName,
                             email= newEmail,
                             level = newLevel,
                             provider= 'arcgis')
arcpy.AddMessage("User " + newUsername +" created successfully!\n")

#Creation of the group if it doesn't exist. Otherwise, adding the project manager in the existing group.
groupName = arcpy.GetParameterAsText(5)
myGroups= gis.groups.search('title:'+groupName)
if len(myGroups) == 0:
    arcpy.AddMessage("Error: The group " + groupName + " does not exist!")
    goodGroup = gis.groups.create(groupName,"python,toronto,uc")
else:
    goodGroup = myGroups[0]
try:
    goodGroup.add_users([newUsername])
    arcpy.AddMessage("User " + newUsername + " added to group "+ goodGroup.title+" sucessfully\n")
except:
    arcpy.AddMessage("Error adding the user " + newUsername + " to group " + goodGroup.title)

#Creation of the feature service for the project using a file geodatabase provided by the user in a zip file.
arcpy.AddMessage("Now, let's create a copy of our template service for the new project\n")
nomProjet = arcpy.GetParameterAsText(6)
descProjet = arcpy.GetParameterAsText(7)
tagsProjet = arcpy.GetParameterAsText(8)
gdbTemplate = arcpy.GetParameterAsText(9)
service_item = gis.content.add({'title':nomProjet,'description':descProjet,'tags':tagsProjet,'type':'File Geodatabase'},data= gdbTemplate,folder='packages')
publishedService = service_item.publish()
arcpy.AddMessage("Service published successfully")
arcpy.AddMessage("Adding service to the group " + goodGroup.title)
publishedService.share(groups=[goodGroup])
