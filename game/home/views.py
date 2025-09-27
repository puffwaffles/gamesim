from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
import pandas as pd
import json
import os
from . import filesfuncs
from . import invfuncs
from . import loginfuncs
import random
import ast

#Used to grab the appropriate function given a view name
def getview(viewname):
    views = {
        "home": home,
        "actualhome": actualhome,
        "gamehome": gamehome,
        "displayinventory": displayinventory,
        "shop": shop,
        "summon": summon,
        "summonresults": summonresults,
        "roster": roster
    }
    return views[viewname]

#Shows up first to offer tutorial. More like a pseudo home. See actualhome for the actual home screen
def home(request):
    tempfile = filesfuncs.cleartemp()
    template = loader.get_template('begin.html')
    return HttpResponse(template.render())

#Prompts user for either login or signup
def promptaccount(request):
    template = loader.get_template('account.html')
    return HttpResponse(template.render())

#Provides signin page
@csrf_protect
def signup(request):
    #Success denotes if new account was successfully created. 0 is uncreated, 1 is success and 2 - 5 denote error 
    success = 0
    username = ""
    password = ""

    #Error codes: 2-> Username already taken, 3-> Missing username, 4-> Missing password, 5-> Missing username and password

    methods = ['Get', 'POST']
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        #Check if there were issues with getting username and password
        if ((username == None or username == "") and (password != None or password != "")):
            success = 3
        elif ((username != None or username != "") and (password == None or password == "")):
            success = 4
        elif((username == None or username == "") and (password == None or password == "")):
            success = 5
        else:
            taken = loginfuncs.checkifuserexists(username)
            if (taken == False):
                loginfuncs.adduser(username, password)
                loginfuncs.createuserfolder(username)
                success = 1
            else:
                success = 2
    context = {
        "username": username,
        "password": password,
        "success": success
    }
    return render(request, 'signup.html', context)



#Provides login page
def login(request):
    #Success denotes if new account was successfully created. 0 is uncreated, 1 is success and 2 - 5 denote error 
    success = 0
    username = ""
    password = ""

    #Error codes: 2-> Wrong username/password, 3-> Missing username, 4-> Missing password, 5-> Missing username and password

    methods = ['Get', 'POST']
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        #Check if there were issues with getting username and password
        if ((username == None or username == "") and (password != None or password != "")):
            success = 3
        elif ((username != None or username != "") and (password == None or password == "")):
            success = 4
        elif((username == None or username == "") and (password == None or password == "")):
            success = 5
        else:
            correct = loginfuncs.verifylogin(username, password)
            if (correct == True):
                success = 1
            else:
                success = 2
    if (success == 1):
        context = {
            "username": username
        }
        return actualhome(request)
    else:
        context = {
            "username": username,
            "password": password,
            "success": success
        }
        return render(request, 'login.html', context)


#Home-> Allows you to access load saves, create a save and delete a save functions
def actualhome(request):
    methods = ['Get']
    #Reset temp file
    tempfile = filesfuncs.cleartemp()
    template = loader.get_template('start.html')
    return HttpResponse(template.render())

#Tutorial-> Displays pages for tutorial to explain parts of the website
@csrf_protect
def tutorial(request):
    methods = ['Get', 'POST']
    page = 1
    previouspage = 0
    nextpage = 2

    
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    if (len(tempcontents) > 0):
        tutorialexit = tempcontents["Contents"]["Tutorialsite"]
        #tutorialexit = getview(tempcontents["Contents"]["Tutorialsite"])
    else:
        tutorialexit = "actualhome"
    
    #Tutorial contains a set of pages. Page items represents the contents of these pages. Each page contains a set of <title, text> pairs
    newcontents = filesfuncs.getfile("tutorial", r'tutorial file/')
    totalpages = len(newcontents)
    pageitems = newcontents[str(page)] 

    if request.method == 'POST':
        
        #Acquire page numbers
        page = int(request.POST.get("newpage"))
        previouspage = page - 1
        nextpage = page + 1
        
        pageitems = newcontents[str(page)]

    context = {
        "tutorialexit": tutorialexit,
        "page": page, 
        "pageitems": pageitems, 
        "previouspage": previouspage, 
        "nextpage": nextpage, 
        "totalpages": totalpages
    }
    return render(request, 'tutorial.html', context)

#Set temp file
def inittemp(savename): 
    saveslist = filesfuncs.acquirefiles()
    newcontents = filesfuncs.getfile(savename, r'save files/')
    tempfile = filesfuncs.updatetemp(savename, newcontents)
    pass  

#Allows you to access your saves
@csrf_protect
def gamehome(request):

    #Initialize temp file first when we first go to gamehome
    tempinit = "False"
    #Use post to save if save button is pressed
    tempsave = "False"
    if request.method == 'POST':
        tempinit = request.POST.get("tempinit")
        if (tempinit == "True"):
            savename = request.POST.get("savename")
            inittemp(savename)
        else:
            tempsave = request.POST.get("savetemp")
            if(tempsave == "True"):
                savetemp()



    panel = filesfuncs.panelitems()
    context = {
        "username": panel["Username"], 
        "level": panel["Level"], 
        "coins": panel["Coins"], 
        "jewels": panel["Jewels"], 
        "realmoney": panel["Real Money Spent"]
    } 
    filesfuncs.updatetutorial("gamehome")
    methods = ['GET', 'POST']

    return render(request, 'gamehome.html', context)

#Update current save to temp contents
def savetemp():
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    savedfile = filesfuncs.updatesave(tempcontents)
    pass

def maketransaction(item, operation, amount):
    success = True
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    savename = tempcontents["Save Name"]

    if (item != "Real Money Spent" and operation != "*"):
        amount = int(amount)
    else:
        amount = round(float(amount), 2)

    match operation:
        case "+":
            tempcontents["Contents"][item] = tempcontents["Contents"][item] + amount
        case "-":
            if (checktransaction(item, amount)):
                tempcontents["Contents"][item] = tempcontents["Contents"][item] - amount 
            else:
                success = False
        case "*":
            if (item != "Real Money Spent"):
                tempcontents["Contents"][item] = int(float(tempcontents["Contents"][item]) * amount)
            else:
                tempcontents["Contents"][item] = round(float(tempcontents["Contents"][item]) * amount, 2)
        case _:
            tempcontents["Contents"][item] = amount

    tempfile = filesfuncs.updatetemp(savename, tempcontents["Contents"])

    return success

def checktransaction(currency, amount):
    success = False
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    
    if (tempcontents["Contents"][currency] - amount >= 0):
        success = True
    return success

#Allows user to select a save file to start playing
def loadsaves(request):
    methods = ['Get']
    saveslistkeys = filesfuncs.acquirefiles().keys()
    savenames = []
    for saves in saveslistkeys:
        savenames.append(saves[:-5])
    savenames.sort()
    return render(request, 'loadsaves.html', {"saves": savenames})

#Allows user to type in username to create a new save. Determines if username is entered and reports success
@csrf_protect
def createsave(request):
    methods = ['Get', 'POST']
    saveslist = filesfuncs.acquirefiles()
    error = False
    create = False
    user = ""
    if request.method == 'POST':
        user = request.POST.get("Username")
        valid = filesfuncs.userexists(saveslist, user)
        if (valid == True):
            create = True
            saveslist = filesfuncs.makenewfile(saveslist, user)
        else:
            error = True
    return render(request, 'createsave.html', {"saves": saveslist, "error": error,  "create": create, "user": user})

#Handles reward giving for releasing characters
def releasecharacter(serial):
    currency = "Coins"
    amount = 1000
    operation = "+"
    success = True

    rarity = invfuncs.serialgetrarity(serial)
    if (rarity < 1):
        amount = 0
        maketransaction(item, operation, amount)
        success = False
    elif (rarity < 3):
        amount = amount + random.randint(0, int(amount / 2))
        maketransaction(currency, operation, amount)
        temp = removecharacter(serial)
    else:
        currency = "Jewels"
        amount = 10 * rarity
        amount = amount + random.randint(0, int(amount / rarity))
        maketransaction(currency, operation, amount)
        temp = removecharacter(serial)

    return success

#Handles removing character given serial number
def removecharacter(serial):
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    savename = tempcontents["Save Name"]
    inventory = tempcontents["Contents"]["Inventory"]
    if (serial in inventory):
        del inventory[serial]
    tempcontents["Contents"]["Inventory"] = inventory
    tempfile = filesfuncs.updatetemp(savename, tempcontents["Contents"])
    return tempfile

#Displays the inventory page
@csrf_protect
def displayinventory(request):
    methods = ['Get', 'POST']

    inventorychars = filesfuncs.gettempcomponent("Inventory")
    numchars = len(inventorychars)
    transaction = "False"
    success = True
    showselect = False
    tempsave = "False"
    released = False
    filesfuncs.updatetutorial("displayinventory")

    selected = {
        "Name": "",
        "Serial": 0,
        "Picture": "",
        "Type": "",
        "Rarity": 0
    }

    if request.method == 'GET':
        if (numchars > 0):
            showselect = True
            indices = [int(nums) for nums in inventorychars.keys()] 
            firstone = str(min(indices))
            selected = inventorychars[firstone]
            selected["Serial"] = firstone
            selected["Raritylist"] = [0] * selected["Rarity"]

    if request.method == 'POST':
        tempsave = request.POST.get("savetemp")
        if (tempsave == "True"):
            savetemp()
            if (numchars > 0):
                showselect = True
                #Display character that was selected before save
                selectedserial = int(request.POST.get("Pickserial"))
                #Make sure selectedserial is actually a number
                if (isinstance(selectedserial, int)):
                    #Check if selected serial is within the list indices
                    if (selectedserial >= 0 and selectedserial < len(inventorychars)):
                        selectedserial = str(selectedserial)
                        selected = inventorychars[selectedserial]
                        selected["Serial"] = selectedserial
                        selected["Raritylist"] = [0] * selected["Rarity"]
                    else:
                        indices = [int(nums) for nums in inventorychars.keys()] 
                        firstone = str(min(indices))
                        selected = inventorychars[firstone]
                        selected["Serial"] = firstone
                        selected["Raritylist"] = [0] * selected["Rarity"]
                else:
                    indices = [int(nums) for nums in inventorychars.keys()] 
                    firstone = str(min(indices))
                    selected = inventorychars[firstone]
                    selected["Serial"] = firstone
                    selected["Raritylist"] = [0] * selected["Rarity"]
        #Handle releasing character
        elif (request.POST.get("released") == "True"):
            serial = request.POST.get("Pickserial")
            #Check if serial can be passed off to release character
            if (serial.isnumeric()):
                released = releasecharacter(serial)
                inventorychars = filesfuncs.gettempcomponent("Inventory")
                numchars = len(inventorychars)
                if (numchars > 0):
                    indices = [int(nums) for nums in inventorychars.keys()]
                    newone = 0
                    for i in indices:
                        if (i < int(serial)):
                            newone = i
                        else:
                            break
                    newone = max(min(indices), newone)
                    newone = str(newone)
                    selected = inventorychars[newone]
                    selected["Serial"] = newone
                    selected["Raritylist"] = [0] * selected["Rarity"]
                    showselect = True
                else:
                    showselect = False
            #Assume you can only access release button if there are characters that can be released
        #For switching selected character
        else:
            if (numchars > 0):
                showselect = True
                
                try:
                    selected = ast.literal_eval(request.POST.get("Picked"))
                except:
                    indices = [int(nums) for nums in inventorychars.keys()] 
                    firstone = str(min(indices))
                    selected = inventorychars[firstone]
                    selected["Serial"] = firstone
                    selected["Raritylist"] = [0] * selected["Rarity"]
                    
                    print(f" rarity = {selected["Rarity"]}")

                    print(f"First selected[{selected["Serial"]}] is {selected["Name"]}")
                else:
                    selectedserial = request.POST.get("Pickserial")
                    selected["Serial"] = selectedserial
                    selected["Raritylist"] = [0] * selected["Rarity"]
                    print(f" rarity = {selected["Rarity"]}")
                    print(f" rarity = {selected["Raritylist"]}")
                    print(f"New selected[{selected["Serial"]}] is {selected["Name"]}")
                
                #Transaction for increasing inventory size
                transaction = request.POST.get("transaction")
                if(transaction == "True"):
                    transaction = request.POST.get("transaction")
                    success = maketransaction("Coins", "-", 10000)
                    if (success == True):
                        invfuncs.increaseinventory()
    panel = filesfuncs.panelitems()

    context = {
        "username": panel["Username"], 
        "level": panel["Level"], 
        "coins": panel["Coins"], 
        "jewels": panel["Jewels"], 
        "realmoney": panel["Real Money Spent"],
        "inventorychars": inventorychars, 
        "showselect": showselect, 
        "selected": selected, 
        "success": success,
        "inventorysize": panel["Inventory Max Size"],
        "numchars": numchars
    } 

    return render(request, 'inventory.html', context)

#Provides menu for deleting saves
@csrf_protect
def deletesave(request):
    methods = ['Get', 'POST']
    saveslist = filesfuncs.acquirefiles()
    savenames = filesfuncs.filessorted(saveslist)
    
    delete = False
    file = ""

    if request.method == 'POST':
        file = request.POST.get("savefile")
        delete = True        
        saveslist = filesfuncs.removeoldfile(saveslist, file)
        savenames = filesfuncs.filessorted(saveslist)
        
    return render(request, 'deletesave.html', {"saves": savenames,  "delete": delete, "file": file})

#Function for processing transaction values from post request
def processtransactionvalues(request, currency, operation, amount):
    values = []
    if (request.method == "POST"):
        currency = request.POST.get(currency)
        operation = request.POST.get(operation)
        amount = request.POST.get(amount)
        values = [currency, operation, amount]
    return values

#Represents a shop that allows you to buy things
@csrf_protect
def shop(request):
    methods = ['Get', 'POST']

    inventorychars = filesfuncs.gettempcomponent("Inventory")
    numchars = len(inventorychars)
    transaction = "False"
    filesfuncs.updatetutorial("shop")

    #Default that represents no transaction that has taken place. -1 is failure and 1 is success
    success = 0

    #Flag for determining if save was made
    tempsave = "False"

    #Default tab is first one
    defaulttab = "Coins"

    if request.method == "GET":
        defaulttab = "Coins"
        print("Defaulttab is set to coins")

    #Handles chosen transactions and saving
    if request.method == 'POST':
        print(f"Post request made!")

        #Retrieve the tab we are on
        defaulttab = request.POST.get("defaulttab")
        if (defaulttab == None):
            defaulttab = "Coins"
        print(f"defaulttab: {defaulttab}")

        tempsave = request.POST.get("savetemp")
        if (tempsave == "True"):
            savetemp()
        else:
            #If we save, we shouldn't be doing a transaction at the same time
            tempsave = request.POST.get("savetemp")
            if (tempsave == "True"):
                savetemp()
            #Transaction
            else:    
                try:
                    transaction = request.POST.get("transaction")
                except: 
                    success = 0
                    defaulttab = "Coins"
                else:
                    if (transaction == "True"):
                        print(f"Transaction made!")
                        values = processtransactionvalues(request, "currency1", "operation1", "amount1")
                        success = invfuncs.intbool(maketransaction(values[0], values[1], values[2]))
                        if (success == 1):
                            print(f"transaction went through!")
                            values = processtransactionvalues(request, "currency2", "operation2", "amount2")
                            success = invfuncs.intbool(maketransaction(values[0], values[1], values[2])) 
                        else:
                            defaulttab = "Coins"

    panel = filesfuncs.panelitems()
    context = {
        "defaulttab": defaulttab,
        "username": panel["Username"], 
        "level": panel["Level"], 
        "coins": panel["Coins"], 
        "jewels": panel["Jewels"], 
        "realmoney": panel["Real Money Spent"],
        "inventorychars": inventorychars, 
        "success": success,
        "inventorysize": panel["Inventory Max Size"],
        "numchars": numchars
    } 
    print(f"success: {success}")
    print(f"defaulttab: {defaulttab}")
    return render(request, 'shop.html', context)

#Represents the summons area which allows you to summon more characters
@csrf_protect
def summon(request):
    methods = ['Get', 'POST']

    inventorychars = filesfuncs.gettempcomponent("Inventory")
    numchars = len(inventorychars)
    transaction = "False"
    filesfuncs.updatetutorial("summon")

    #Default that represents no transaction that has taken place. -1 is failure and 1 is success
    success = 0
    failedcurrency = ""
    #Determines if a summon can be made based on inventory capacity
    summonable = True
    summonlist = []

    #Flag for determining if save was made
    tempsave = "False"

    #Handles chosen transactions
    if request.method == 'POST':
        print(f"Post request made!")

        tempsave = request.POST.get("savetemp")
        if (tempsave == "True"):
            savetemp()
        else:
            #Check if transaction value has been set by post request
            try:
                transaction = request.POST.get("transaction")
            except: 
                success = 0
            else:
                if (transaction == "True"):
                    print(f"Transaction made!")
                    #Get information on type of summon to be made
                    summontype = request.POST.get("summontype")
                    summoninfo = invfuncs.summoncomponents()

                    if (summontype in summoninfo.keys()):

                        #Check the amount that will be added to the inventory
                        toadd = summoninfo[summontype]["Number of Summons"]
                        #If there is enough space in inventory, proceed with the transaction
                        if (numchars + toadd <= filesfuncs.gettempcomponent("Inventory Max Size")):
                            print(f"transaction = {True}")
                            summonable = True
                            #Perform transaction changes
                            values = processtransactionvalues(request, "currency1", "operation1", "amount1")
                            failedcurrency = values[0].lower()
                            success = invfuncs.intbool(maketransaction(values[0], values[1], values[2]))

                            if (success == 1):
                                #If transaction can proceed, start summoning characters
                                if (toadd == 1):
                                    types = summoninfo[summontype]["Types"]
                                    baserarities = summoninfo[summontype]["Base Rarities"]
                                    summonlist = invfuncs.summonfor1(types, baserarities)
                                else:
                                    types = summoninfo[summontype]["Types"]
                                    baserarities = summoninfo[summontype]["Base Rarities"]
                                    pityrarities = summoninfo[summontype]["Pity Rarity"]
                                    summonlist = invfuncs.summonfor10(types, baserarities, pityrarities)
                        else:
                            summonable = False
                    else:
                        summonable = False

    panel = filesfuncs.panelitems()
    context = {
        "username": panel["Username"], 
        "level": panel["Level"], 
        "coins": panel["Coins"], 
        "jewels": panel["Jewels"], 
        "realmoney": panel["Real Money Spent"],
        "inventorychars": inventorychars, 
        "success": success,
        "failedcurrency": failedcurrency,
        "summonable": summonable,
        "inventorysize": panel["Inventory Max Size"],
        "numchars": numchars
    }
    
    #Means that characters will be summoned and user will be redirected to summon page
    if (success == 1 and summonable == True):
        return summonresults(request, context, summonlist)
    #Display normal summon menu as usual
    else:
        return render(request, 'summon.html', context)

#Displays the results of the summon
def summonresults(request, context, summonlist):
    newcontext = context
    newcontext["summonlist"] = summonlist
    return render(request, 'summonresults.html', newcontext)

#Represents a shop that allows you to buy things
@csrf_protect
def roster(request):
    methods = ['Get', 'POST']
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    #Get roster from tempfile
    temproster = tempcontents["Contents"]["Chracter Collection"]
    #Get info on whether characters can be claimed
    claimable = len(invfuncs.hasrewards())
    print(f"claimable: {claimable}")
    #Flag for when someone clicks on a character panel in the roster
    claimsingle = "False"
    #Flag for when someone clicks on claim all rewards
    claimall = "False"
    filesfuncs.updatetutorial("roster")

    #Default that represents no transaction that has taken place. -1 is failure and 1 is success
    success = 0

    #Flag for determining if save was made
    tempsave = "False"

    #Default tab is first one
    defaulttab = "Fire"

    if request.method == "GET":
        defaulttab = "Fire"
        print("Defaulttab is set to fire")
    #Handles chosen transactions
    if request.method == 'POST':
        print(f"Post request made!")
        defaulttab = request.POST.get("defaulttab")

        if (defaulttab == None):
            defaulttab = "Fire"
        
        tempsave = request.POST.get("savetemp")
        if (tempsave == "True"):
            savetemp()
        else:

            #Check if someone clicked on a character panel in the roster
            try:
                claimsingle = request.POST.get("claimsingle")
                print(f"claimsingle is {claimsingle}")
            except: 
                print("Except triggered")
                success = 0
                defaulttab = "Fire"

            #Otherwise process claiming for one character
            else:
                if (claimsingle == "True"):
                    defaulttab = "Fire"
                    try:
                        charname = request.POST.get("charname")
                    except: 
                        success = 0
                    else:
                        typeandrarity = invfuncs.gettypeandrarity(charname)
                        typing = typeandrarity["Type"]
                        rarity = typeandrarity["Rarity"]
                        acquired = invfuncs.getrostercharacterstatus(typing, rarity, charname, "Acquired")
                        canclaim = invfuncs.getrostercharacterstatus(typing, rarity, charname, "Claimed")
                        #Check if character has been acquired and can be claimed
                        if (acquired, canclaim):
                            #Retrieve jewel reward for given character
                            amount = invfuncs.newcharacterrewardamount(rarity)
                            #Update roster in tempfile
                            invfuncs.updateroster(typing, rarity, charname, "Claimed")
                            success = invfuncs.intbool(maketransaction("Jewels", "+", amount))
                        else:
                            defaulttab = "Fire"
                else:
                    #Check if someone clicked on claim all rewards
                    try: 
                        claimall = request.POST.get("claimall")
                    except:
                        success = 0
                        defaulttab = "Fire"
                    else:
                        print("Can claim all")
                        if (claimall == "True"):
                            #Retrieve jewel reward for given character. Function also updates roster in tempfile
                            amount = invfuncs.updaterosterandcalcrewards()
                            success = invfuncs.intbool(maketransaction("Jewels", "+", amount))
                        else: 
                            defaulttab = "Fire"

    #Reinitialize to reflect changes
    panel = filesfuncs.panelitems()
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    temproster = tempcontents["Contents"]["Chracter Collection"]
    claimable = len(invfuncs.hasrewards())

    context = {
        "defaulttab": defaulttab,
        "username": panel["Username"], 
        "level": panel["Level"], 
        "coins": panel["Coins"], 
        "jewels": panel["Jewels"], 
        "realmoney": panel["Real Money Spent"],
        "temproster": temproster,
        "claimable": claimable,
        "success": success
    } 
   
    return render(request, 'roster.html', context)