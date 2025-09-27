import json
import os, os.path
import hashlib
from . import filesfuncs

#function for creating hashed hex value
def sha256convert(string):
    return hashlib.sha256(string.encode()).hexdigest()

#Check if username already exists
def checkifuserexists(username):
    exists = False
    users = filesfuncs.getfile("usersfile", r'users/')
    usernameconverted = sha256convert(username)
    if (usernameconverted in users.keys()):
        exists = True
    return exists

#Add username and password to userfile
def adduser(username, password):
    newcontents = filesfuncs.getfile("usersfile", r'users/')
    filename = "usersfile.json"

    usernameconverted = sha256convert(username)
    passwordconverted = sha256convert(password)
    newcontents[usernameconverted] = passwordconverted

    path = filesfuncs.getfolderpath(r'users/')
    newpath = path + filename
    newfile = filesfuncs.replacefile(newcontents, newpath)
    pass

#Retrieve sha256 password for given sha256 username
def getsha256password(sha256username):
    password = ""
    users = filesfuncs.getfile("usersfile", r'users/')
    password = users[sha256username]
    return password

#Verifies if correct username and password were given
def verifylogin(username, password):
    unlocked = False
    exists = checkifuserexists(username)
    if (exists == True):
        sha256username = sha256convert(username)
        sha256password = sha256convert(password)
        if (sha256password == getsha256password(sha256username)):
            unlocked = True
    return unlocked

#Creates new folder for user account
def createuserfolder(username):
    path = filesfuncs.getfolderpath(r'users/')
    path += username
    os.makedirs(path)
    #Create folder for saves
    savepath = path + "/save files"
    os.makedirs(savepath, exist_ok=True)
    #Create folder for temp file
    temppath = path + "/temp file"
    os.makedirs(temppath, exist_ok=True)
    #Create temp file
    newcontents = {}
    newpath = temppath + "/temp.json"
    newfile = filesfuncs.replacefile(newcontents, newpath)
    pass

#Access user folder for given username
def getuserfolder(username):
    path = filesfuncs.getfolderpath(r'users/')
    path = os.path.join(path, username)
    
    return path

#Deletes user folder for given username and updates userfile
def deleteuser(username):
    userpath = getuserfolder(username)
    os.remove(userpath)

    newcontents = filesfuncs.getfile("usersfile", r'users/')
    sha256username = sha256convert(username)
    del newcontents[sha256username]
    filename = "usersfile.json"
    path = filesfuncs.getfolderpath(r'users/')
    newpath = path + filename
    newfile = filesfuncs.replacefile(newcontents, newpath)
    pass

#Access given folder for given username
def getfolderfromuser(folder, username):
    path = getuserfolder(username)
    path = os.path.json(path, folder)
    return path

#Get list of saves for given username folder
def getsaveslist(username):
    saveslist = {
        "Size": 0
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

#Creates new savefile
def createnewsave(username, savename):
    success = False
    saveslist = getsaveslist(username)
    if (saveslist["Size"] < 5):
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
            "Chracter Collection": filesfuncs.developroster()
        }
        savepath = savefilepath(username, savename)
        savefile = replacefile(newcontents, savepath)
        success = True
    return success

#Deletes given savefile 
def deleteoldsave(username, savename):
    success = False
    saveslist = getsaveslist(username)
    if (saveslist["Size"] > 0):
        savepath = savefilepath(username, savename)
        os.remove(savepath)
    return success

#Initialize temp with save file contents
def settemp(savename, savecontents):
    setcontents = {
        "Save Name": savename,
        "Contents": savecontents
    }
    
    setcontents = replacetemp(username, setcontents)
    return setcontents

#Replace temp with new contents and return new contents
def replacetemp(username, contents):
    path = getfolderfromuser("temp file", username)
    path += "temp.json"
    contents = replacefile(contents, path)
    return contents

#Extracts savename for path
def extractsavename(path):
    savename = path[-11:-5]
    return savename

#Retrieves save file path from savename
def savefilepath(username, savename):
    path = getfolderfromuser("folder", username)
    path += username + ".json"
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

#Acquires contents of tempfile (the contents that will be saved to savefile)
def gettempcontents(username):
    path = getfolderfromuser("temp file", username)
    path += "temp.json"
    contents = getjsonfrompath(path)
    tempcontents = contents["Contents"]
    return contents

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




