from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import os, os.path

#Generates path for folder
def getfolderpath(folder):
    filedirectory = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(filedirectory, folder)
    return path

#Grabs contents of given file (excluding extension) from folder
def getfile(filename, folder):
    path = getfolderpath(folder)
    newpath = path + filename + '.json'
    contents = {}
    with open(newpath, "r")  as file: 
        contents = json.load(file)
    return contents

#Overwrites file given contents and filepath
def replacefile(contents, path):
    newfile = json.dumps(contents, indent = 2)
    with open(path, "w") as file:
        file.write(newfile)
    return contents

#Needs to be here since we need to initialize roster while building a new file
#Converts groupedroster.json into a roster dictionary that identifies acquired and nonaquired characters
def developroster():
    orgroster = getfile("groupedroster", r'data/')
    #Iterate for each character and have them preset to not aquired (False)
    for types in orgroster:
        for i in range(1, 6):
            for chars in orgroster[types][str(i)].keys():
                orgroster[types][str(i)][chars]["Acquired"] = False
                orgroster[types][str(i)][chars]["Claimed"] = False
    return orgroster

#Creates folder in given path and returns path
def makefolder(path):
    os.makedirs(path, exist_ok=True)
    return path

#Access user folder for given username
def getuserfolder(username):
    path = getfolderpath(r'users/')
    path = os.path.join(path, username)
    
    return path

#Access given folder for given username
def getfolderfromuser(folder, username):
    path = getuserfolder(username)
    path = os.path.join(path, folder + "/")
    return path

#Get list of saves for given username folder
def getsaveslist(username):
    saveslist = {
        "Size": 0,
        "save 1": None,
        "save 2": None,
        "save 3": None,
        "save 4": None,
        "save 5": None
    }
    #Get path of saves folder 
    path = getfolderfromuser("save files", username)
    #Iterate through files in save files folder
    for files in os.listdir(path):
        #Check for legitimate save files to add to saveslist
        if (files.endswith(".json")):
            currfile = path + "/" + files
            with open(currfile, "r")  as file: 
                filename = extractsavename(files)
                saveslist[filename] = json.load(file)
                saveslist["Size"] += 1
    
    return saveslist

#Retrieves all unused or all used saves depending on status passed in
def getfiltersaves(username, status):
    filtersaveslist = {
        "Size": 0,
    }
    saveslist = getsaveslist(username)
    
    for savenames, saves in saveslist.items():
        if ((savenames != "Size") and ((status == "used" and saveslist[savenames] != None) or (status == "unused" and saveslist[savenames] == None))):
            filtersaveslist[savenames] = saves
            filtersaveslist["Size"] += 1
    return filtersaveslist

#Creates new savefile if save is unused
def createnewsave(username, savename):
    success = False
    saveslist = getfiltersaves(username, "unused")
    if (saveslist["Size"] > 0 and savename in saveslist.keys()):
        newcontents = {
            "Username": username,
            "Level": 1,
            "Coins": 100000,
            "Jewels": 500,
            "Real Money Spent": 0,
            "Inventory": {},
            "Inventory Max Size": 20,
            "Serial Number": 1,
            "Tutorialsite": "actualhome",
            "Chracter Collection": developroster()
        }
        savepath = savefilepath(username, savename)
        savefile = replacefile(newcontents, savepath)
        success = True
    return success

#Deletes given savefile 
def deleteoldsave(username, savename):
    success = False
    saveslist = getfiltersaves(username, "used")
    if (saveslist["Size"] > 0 and savename in saveslist.keys()):
        savepath = savefilepath(username, savename)
        os.remove(savepath)
    return success

#Initialize temp with save file contents
def settemp(username, savename, savecontents):
    setcontents = {
        "Username": username,
        "Save Name": savename,
        "Contents": savecontents
    }
    
    setcontents = replacetemp(username, setcontents)
    return setcontents

#Replace temp with new contents and return new contents
def replacetemp(username, contents):
    path = getfolderfromuser("temp file", username)
    path += "/temp.json"
    contents = replacefile(contents, path)
    return contents

#Extracts savename for path
def extractsavename(path):
    savename = path[-11:-5]
    return savename

#Retrieves save file path from savename
def savefilepath(username, savename):
    path = getfolderfromuser("save files", username)
    path += savename + ".json"
    return path

#Returns contents of json file given path
def getjsonfrompath(path):
    contents = contents = {}
    with open(path, "r")  as file: 
        contents = json.load(file)
    return contents

#Acquires contents of savefile
def getsavefilecontents(username, savename):
    path = savefilepath(username, savename)
    contents = getjsonfrompath(path)
    return contents

#Returns all contents of entire temp json including save name, username and contents
def gettemp(username):
    path = getfolderfromuser("temp file", username)
    path += "/temp.json"
    contents = getjsonfrompath(path)
    return contents

#Grabs savename from tempfile
def gettempsavename(username):
    contents = gettemp(username)
    savename = contents["Save Name"]
    return savename

#Acquires contents of tempfile (the contents that will be saved to savefile)
def gettempcontents(username):
    contents = gettemp(username)
    tempcontents = contents["Contents"]
    return tempcontents

#Saves temp content to save file
def savetofile(username, savename):
    tempcontents = gettempcontents(username)
    savepath = savefilepath(username, savename)
    newcontents = replacefile(tempcontents, savepath)
    return newcontents

#Acquire specific value from temp's contents
def gettempitem(username, item):
    item = gettempcontents(username)[item]
    return item

#Acquire panel items
def getpanelitems(username):
    panel = {
        "Username": gettempitem(username, "Username"),
        "Level": gettempitem(username, "Level"),
        "Coins": gettempitem(username, "Coins"),
        "Jewels": gettempitem(username, "Jewels"),
        "Real Money Spent": gettempitem(username, "Real Money Spent"),
        "Inventory Max Size": gettempitem(username, "Inventory Max Size")
    }
    return panel

######################################################################################
