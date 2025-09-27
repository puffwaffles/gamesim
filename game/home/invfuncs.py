import json
import os, os.path
from . import filesfuncs
import random

#Returns contents of summons json file
def summoncomponents():
    value = filesfuncs.getfile("summons", r'data/')
    return value


#Determines value by probability
def pickval(probslist):
    val = None
    probstart = 0
    calcprob = random.random()
    lastval = ""

    for keys, probs in probslist.items():
        lastval = keys
        #Json for summons uses string arithmetic operations to calculate rational probabilities
        if (isinstance(probs, str)):
            #Convert to fractional value
            probs = eval(probs)

        if (probs + probstart >= calcprob):
            val = keys
            break
        else:
            probstart += probs
    
    #If the probabilties don't fully add up to 1 due to round off errors, use last one in list as default
    if (val == None):
        val = lastval

    return val

#Converts value into 1 or -1 to denote success or failure
def intbool(value):
    if (value == True):
        return 1
    else:
        return -1

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

    #For newly acquired characters, update the roster
    isnew = getrostercharacterstatus(typing, rarity, charname, "Acquired")
    if (isnew == False):
        updateroster(typing, rarity, charname, "Acquired")

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


#Adds 10 characters to inventory
def summonfor10(types, baserarities, pityrarity):
    roster = filesfuncs.getfile("roster", r'data/')
    pity = random.randint(1, 10)
    summoned = []

    for i in range(1, 11):    
        if (i == pity):
            charname = pickchar(types, pityrarity)
            updatetempinv(charname)
            summoned.append(roster[charname])
        else:
            charname = pickchar(types, baserarities)
            updatetempinv(charname)
            summoned.append(roster[charname])
    return summoned

#Adds 1 character to inventory
def summonfor1(types, baserarities):
    roster = filesfuncs.getfile("roster", r'data/')
    summoned = []
    charname = pickchar(types, baserarities)
    updatetempinv(charname)
    summoned.append(roster[charname])

    return summoned

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

#Returns rarity given character serial number
def serialgetrarity(serial):
    rarity = 0
    numchars = len(filesfuncs.gettempcomponent("Inventory"))
    if (numchars > 0 and serial.isnumeric()):
        tempcontents = filesfuncs.getfile("temp", r'temp file/')
        if (serial in tempcontents["Contents"]["Inventory"]):
            rarity = tempcontents["Contents"]["Inventory"][serial]["Rarity"]
    return rarity


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

#Increases current inventory size
def increaseinventory():
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    tempcontents["Contents"]["Inventory Max Size"] += 10
    tempsavename = tempcontents["Save Name"]
    newtemp = filesfuncs.updatetemp(tempsavename, tempcontents["Contents"]) 

    pass

#Organizes roster characters by type and rarity
def organizeroster():
    roster = filesfuncs.getfile("roster", r'data/')
    organizedroster = {}
    typelist = ["Fire", "Water", "Wood", "Light", "Dark"]
    #Create groupings for types and rarities
    for types in typelist:
        organizedroster[types] = {}
        for i in range(5, 0, -1):
            organizedroster[types][i] = {}
    
    #Go through roster to add character to appropriate type and rarity group
    for charnames, charinfo in roster.items():
        typing = charinfo["Type"]
        rarity = charinfo["Rarity"]
        organizedroster[typing][rarity][charnames] = charinfo
    
    #Put everything in organized order
    for types in typelist:
        for i in range(5, 0, -1):
            organizedroster[types][i] = dict(sorted(organizedroster[types][i].items()))
    
    path = filesfuncs.getfolderpath(r'data/')
    newpath = path + 'groupedroster.json'

    reorganized = filesfuncs.replacefile(organizedroster, newpath)
    
    pass

#Retrieves character type and rarity
def gettypeandrarity(charname):
    typeandrarity = {}
    roster = filesfuncs.getfile("roster", r'data/')
    if (charname in roster.keys()):
        typeandrarity["Type"] = roster[charname]["Type"]
        typeandrarity["Rarity"] = str(roster[charname]["Rarity"])
    return typeandrarity

#Finds out if character has been newly aquired (status = "Acquired") or had its rewards claimed (status = "Claimed")
def getrostercharacterstatus(types, rarity, charname, status):
    isstatus = False
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    orgroster = tempcontents["Contents"]["Chracter Collection"]
    if (charname in orgroster[types][str(rarity)].keys()):
        isstatus = orgroster[types][rarity][charname][status] 
    return isstatus

#Updates roster when new char is added to inventory. Only called if there is actually a new character
def updateroster(types, rarity, charname, status):
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    savename = tempcontents["Save Name"]
    tempcontents["Contents"]["Chracter Collection"][types][str(rarity)][charname][status] = True
    tempfile = filesfuncs.updatetemp(savename, tempcontents["Contents"])

    pass

#Calculates amount of jewels given based on rarity
def newcharacterrewardamount(rarity):
    amount = 0
    match rarity:
        case "1":
            amount = 5
        case "2":
            amount = 10
        case "3":
            amount = 20
        case "4":
            amount = 60
        case "5":
            amount = 120
        case _:
            amount = 0
    return amount

#Updates each characters whose rewards have not yet been claimed
def updaterosterandcalcrewards():
    totalamount = 0
    claimable = hasrewards()
    #Iterate through characters to find ones without claimed rewards. Calculate reward amount and update claimed reward status
    for characters in claimable:
        #claimable tuples are character name, type, rarity
        if (getrostercharacterstatus(characters[1], characters[2], characters[0], "Claimed") == False):
            print(f"Can claim {characters[0]}")
            totalamount += newcharacterrewardamount(characters[2])
            #Update temp file
            updateroster(characters[1], characters[2], characters[0], "Claimed")

    return totalamount

#Checks if there are any rewards to claim and returns a list of characters whose rewards can be claimed
def hasrewards():
    claimable = []
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    temproster = tempcontents["Contents"]["Chracter Collection"]

    for types in temproster.keys():
        for i in range(1, 6):
            for charname in temproster[types][str(i)].keys():
                charinfo = [charname, types, str(i)]
                aquired = getrostercharacterstatus(types, str(i), charname, "Acquired")
                claims = getrostercharacterstatus(types, str(i), charname, "Claimed")
                if (aquired == True and claims == False):
                    claimable.append(charinfo)
    print(len(claimable))
    return claimable



#organizeroster()
#testpicker()
#summonbatch1to3()