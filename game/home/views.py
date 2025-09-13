from django.shortcuts import render
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
import ast

#Used to grab the appropriate function given a view name
def getview(viewname):
    views = {
        "home": home,
        "actualhome": actualhome,
        "gamehome": gamehome,
        "displayinventory": displayinventory
    }
    return views[viewname]

#Shows up first to offer tutorial. More like a pseudo home. See actualhome for the actual home screen
def home(request):
    tempfile = filesfuncs.cleartemp()
    template = loader.get_template('begin.html')
    return HttpResponse(template.render())

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
    return render(request, 'tutorial.html', {"page": page, "pageitems": pageitems, "previouspage": previouspage, "nextpage": nextpage, "totalpages": totalpages})

#Set temp file
@csrf_protect
def inittemp(request):
    methods = ['POST']
    if request.method == 'POST':
        savename = request.POST.get("savename")
        saveslist = filesfuncs.acquirefiles()
        newcontents = filesfuncs.getfile(savename, r'save files/')
        tempfile = filesfuncs.updatetemp(savename, newcontents)
       
    return gamehome(request)

def gamehome(request):
    username = filesfuncs.gettempcomponent("Username")
    level = filesfuncs.gettempcomponent("Level")
    coins = filesfuncs.gettempcomponent("Coins")
    jewels = filesfuncs.gettempcomponent("Jewels")
    return render(request, 'gamehome.html', {"username": username, "level": level, "coins": coins, "jewels": jewels})

#Update current save to temp contents
@csrf_protect
def savetemp(request):
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    savedfile = filesfuncs.updatesave(tempcontents)
    nextfunc = gamehome
    if request.method == 'POST':
        funcname = request.POST.get("funcname")
        nextfunc = getview(funcname)

    return nextfunc(request)

#Testing purposes for adding to jewels amount
@csrf_protect
def changeamount(request):
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    savename = tempcontents["Save Name"]
    nextfunc = gamehome

    if request.method == 'POST':
        funcname = request.POST.get("funcname")
        operation = request.POST.get("operation")
        item = request.POST.get("item")
        amount = request.POST.get("amount")

        tempval = tempcontents["Contents"][item]
        
        match operation:
            case "+":
                tempcontents["Contents"][item] = tempcontents["Contents"][item] + int(amount)
            case "-":
                tempcontents["Contents"][item] = tempcontents["Contents"][item] - int(amount)
            case "*":
                tempcontents["Contents"][item] = int(float(tempcontents["Contents"][item]) * float(amount))
            case _:
                tempcontents["Contents"][item] = int(amount)

        if (tempcontents["Contents"][item] < 0):
            tempcontents["Contents"][item] = tempval

        tempfile = filesfuncs.updatetemp(savename, tempcontents["Contents"])
        
        nextfunc = getview(funcname)

    return nextfunc(request)

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

@csrf_protect
def releasecharacter(request):
    nextfunc = displayinventory
    methods = ['POST']

    if request.method == 'POST':
        serial = request.POST.get("Pickserial")
        success = invfuncs.release(serial)
        funcname = "displayinventory"
        nextfunc = getview(funcname)

    return nextfunc(request)

#Displays the inventory page
@csrf_protect
def displayinventory(request):
    methods = ['Get', 'POST']

    username = filesfuncs.gettempcomponent("Username")
    level = filesfuncs.gettempcomponent("Level")
    coins = filesfuncs.gettempcomponent("Coins")
    jewels = filesfuncs.gettempcomponent("Jewels")

    inventorychars = filesfuncs.gettempcomponent("Inventory")

    showselect = False

    selected = {
        "Name": "",
        "Serial": 0,
        "Picture": "",
        "Type": "",
        "Rarity": 0
    }

    if request.method == 'GET':
        if (len(inventorychars) > 0):
            showselect = True
            indices = [int(nums) for nums in inventorychars.keys()] 
            firstone = str(min(indices))
            selected = inventorychars[firstone]
            selected["Serial"] = firstone

    if request.method == 'POST':
        if (len(inventorychars) > 0):
            showselect = True
            try:
                selected = ast.literal_eval(request.POST.get("Picked"))
            except:
                indices = [int(nums) for nums in inventorychars.keys()] 
                firstone = str(min(indices))
                selected = inventorychars[firstone]
                selected["Serial"] = firstone
                print(f"First selected[{selected["Serial"]}] is {selected["Name"]}")
            else:
                selectedserial = int(request.POST.get("Pickserial"))
                selected["Serial"] = selectedserial
                print(f"New selected[{selected["Serial"]}] is {selected["Name"]}")
        
    return render(request, 'inventory.html', {"username": username, "level": level, "coins": coins, "jewels": jewels, "inventorychars": inventorychars, "showselect": showselect, "selected": selected})

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


