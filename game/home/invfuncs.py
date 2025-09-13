import json
import os, os.path
from . import filesfuncs
import random

#Determines value by probability
def pickval(probslist):
    val = None
    probstart = 0
    calcprob = random.random()
    lastval = ""

    for keys, probs in probslist.items():
        lastval = keys
        if (probs + probstart >= calcprob):
            val = keys
            break
        else:
            probstart += probs
    
    #If the probabilties don't fully add up to 1 due to round off errors, use last one in list as default
    if (val == None):
        val = lastval

    return val


#Pick random char based on type probabilities and rarity probabilities (in terms of decimals from 0 to 1)
def pickchar(types, raritieslist):
    charname = ""
    orgroster = filesfuncs.getfile("groupedroster", r'data/')
    typing = ""
    rarity = 0

    #Determine type
    typing = pickval(types)

    #Determine rarity
    rarity = pickval(raritieslist)

    #Select the list of characters with the appropriate typing and rarity
    availablelist = []
    if (len(orgroster[typing][rarity]) > 0):
        for names in orgroster[typing][rarity].keys():
            availablelist.append(names)
            sorted(availablelist)

    #Select a random character in the list by index
    if (len(availablelist) >= 1):
        randindex = random.randint(0, len(availablelist) - 1)
        charname = availablelist[randindex]

    return charname

#Picks from a given list
def pickcharfromlist(types, raritieslist, speciallist):
    charname = ""
    orgroster = filesfuncs.getfile("groupedroster", r'data/')
    typing = ""
    rarity = 0

    #Determine type
    typing = pickval(types)

    #Determine rarity
    rarity = pickval(raritieslist)

    #Select the list of characters with the appropriate typing and rarity
    availablelist = []
    if (len(orgroster[typing][rarity]) > 0):
        for names in orgroster[typing][rarity].keys():
            availablelist.append(names)
            
    
    #Limit availablelist to characters in the special list
    available = list(availablelist & speciallist)
    sorted(availablelist)

    #Select a random character in the list by index
    if (len(availablelist) >= 1):
        randindex = random.randint(0, len(availablelist) - 1)
        charname = availablelist[randindex]

    return charname

#Just testing for basic summon from 1-3
def testpicker():
    types = {
        "Fire": (1.0 / 3.0),
        "Water": (1.0 / 3.0),
        "Wood": (1.0 / 3.0)
    }
    rarities = {
        "1": 0.6,
        "2": 0.3,
        "3": 0.1
    }
    charname = pickchar(types, rarities)
    if (charname == ""):
        print(f"No such character exists for given type and rarity\n")
    else:
        print("\n")
        print(f"Summoned character {charname} \n")
    pass

#Test batch summon
def summonbatch1to3():
    types = {
        "Fire": (1.0 / 3.0),
        "Water": (1.0 / 3.0),
        "Wood": (1.0 / 3.0)
    }
    baserarities = {
        "1": 0.6,
        "2": 0.3,
        "3": 0.1
    }
    pityrarity = {
        "2": 0.8,
        "1": 0.2
    }
    pity = random.randint(1, 10)
    print("\n")
    for i in range(1, 10):    
        if (i == pity):
            charname = pickchar(types, pityrarity)
            #print(f"Pity character summoned {charname}\n")
        else:
            charname = pickchar(types, baserarities)
            #print(f"Summoned character {charname} \n")
    pass

#Creates character contents given name from roster
def buildchar(charname):
    roster = filesfuncs.getfile("roster", r'data/')
    charcontents = roster[charname]
    #Include the name of the character as part of the contents
    charcontents["Name"] = charname
    return charcontents

#Update inventory with new character. 
def updatetempinv(charname):
    success = False
    numchars = len(filesfuncs.gettempcomponent("Inventory"))
    maxsize = filesfuncs.gettempcomponent("Inventory Max Size")
    
    if (numchars < maxsize):
        tempcontents = filesfuncs.getfile("temp", r'temp file/')
        #Get character info and serial number
        charinfo = buildchar(charname)
        charserial = filesfuncs.gettempcomponent("Serial Number")
        #Add character entry to temp contents 
        tempcontents["Contents"]["Inventory"][charserial] = charinfo
        #Increment serial number
        tempcontents["Contents"]["Serial Number"] = charserial + 1
        #Update temp file with new temp contents
        tempsavename = tempcontents["Save Name"]
        newtemp = filesfuncs.updatetemp(tempsavename, tempcontents["Contents"]) 
        success = True
        
    return success

#Removes character given character serial number
def release(serial):
    success = False
    numchars = len(filesfuncs.gettempcomponent("Inventory"))
    
    if (numchars > 0):
        tempcontents = filesfuncs.getfile("temp", r'temp file/')
        #Remove character with given serial number from temp dictionary
        del tempcontents["Contents"]["Inventory"][serial]
        #Update temp file with new temp contents
        tempsavename = tempcontents["Save Name"]
        newtemp = filesfuncs.updatetemp(tempsavename, tempcontents["Contents"]) 
        success = True

    return success

#Organizes roster characters by type and rarity
def organizeroster():
    roster = filesfuncs.getfile("roster", r'data/')
    organizedroster = {}
    typelist = ["Fire", "Water", "Wood", "Light", "Dark"]
    #Create groupings for types and rarities
    for types in typelist:
        organizedroster[types] = {}
        for i in range(1, 6):
            organizedroster[types][i] = {}
    
    #Go through roster to add character to appropriate type and rarity group
    for charnames, charinfo in roster.items():
        typing = charinfo["Type"]
        rarity = charinfo["Rarity"]
        organizedroster[typing][rarity][charnames] = charinfo
    
    #Put everything in organized order
    for types in typelist:
        for i in range(1, 6):
            organizedroster[types][i] = dict(sorted(organizedroster[types][i].items()))
    
    path = filesfuncs.getfolderpath(r'data/')
    newpath = path + 'groupedroster.json'

    reorganized = filesfuncs.replacefile(organizedroster, newpath)
    
    pass

#organizeroster()
#testpicker()
#summonbatch1to3()