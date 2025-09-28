import json
import os, os.path, shutil
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
    return username

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
    path = filesfuncs.makefolder(path)
    #Create folder for saves
    savepath = filesfuncs.makefolder(path + "/save files")
    #Create folder for temp file
    temppath = filesfuncs.makefolder(path + "/temp file")
    #Create temp file
    newcontents = {}
    newfile = filesfuncs.replacefile(newcontents, temppath + "/temp.json")
    pass

#Deletes user folder for given username and updates userfile
def deleteuser(username):
    userpath = filesfuncs.getuserfolder(username)
    shutil.rmtree(userpath)

    newcontents = filesfuncs.getfile("usersfile", r'users/')
    sha256username = sha256convert(username)
    del newcontents[sha256username]
    filename = "usersfile.json"
    path = filesfuncs.getfolderpath(r'users/')
    newpath = path + filename
    newfile = filesfuncs.replacefile(newcontents, newpath)
    pass

