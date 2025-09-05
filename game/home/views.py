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

#Used to grab the appropriate function given a view name
def getview(viewname):
    views = {
        "home": home,
        "gamehome": gamehome 
    }
    return views[viewname]

#Home-> Allows you to access load saves, create a save and delete a save functions
def home(request):
    methods = ['Get']
    #Reset temp file
    tempfile = filesfuncs.cleartemp()
    template = loader.get_template('start.html')
    return HttpResponse(template.render())

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
    username = filesfuncs.getfile("temp", r'temp file/')["Contents"]["Username"]
    level = filesfuncs.getfile("temp", r'temp file/')["Contents"]["Level"]
    coins = filesfuncs.getfile("temp", r'temp file/')["Contents"]["Coins"]
    jewels = filesfuncs.getfile("temp", r'temp file/')["Contents"]["Jewels"]
    return render(request, 'gamehome.html', {"username": username, "level": level, "coins": coins, "jewels": jewels})

#Update current save to temp contents
@csrf_protect
def savetemp(request):
    tempcontents = filesfuncs.getfile("temp", r'temp file/')
    savedfile = filesfuncs.updatesave(tempcontents)
    nextfunc = gamehome
    if request.method == 'POST':
        funcname = request.POST.get("funcname")
        nextfunct = getview(funcname)

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
        
        match operation:
            case "+":
                tempcontents["Contents"][item] = tempcontents["Contents"][item] + int(amount)
            case "-":
                tempcontents["Contents"][item] = tempcontents["Contents"][item] - int(amount)
            case "*":
                tempcontents["Contents"][item] = int(float(tempcontents["Contents"][item]) * float(amount))
            case _:
                tempcontents["Contents"][item] = int(amount)

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
def deletesave(request):
    methods = ['Get', 'POST']
    saveslist = filesfuncs.acquirefiles()
    savenames = filesfuncs.filessorted(saveslist)
    
    delete = False
    file = ""

    if request.method == 'POST':
        file = request.POST.get("savefile")
        print(file)
        delete = True        
        saveslist = filesfuncs.removeoldfile(saveslist, file)
        savenames = filesfuncs.filessorted(saveslist)
        
    return render(request, 'deletesave.html', {"saves": savenames,  "delete": delete, "file": file})


