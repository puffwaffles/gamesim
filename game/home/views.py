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

def home(request):
    methods = ['Get']
    template = loader.get_template('start.html')
    return HttpResponse(template.render())


def loadsaves(request):
    methods = ['Get']
    saveslistkeys = filesfuncs.acquirefiles().keys()
    savenames = []
    for saves in saveslistkeys:
        savenames.append(saves[:-5])
    return render(request, 'loadsaves.html', {"saves": savenames})

@csrf_protect
def createsave(request):
    methods = ['Get', 'POST']
    saveslist = filesfuncs.acquirefiles()
    error = False
    create = False
    if request.method == 'GET':
        print("Triggered get")
        return render(request, 'createsave.html', {"saves": saveslist, "error": error,  "create": create, "user": ""})
    if request.method == 'POST':
        print("Triggered post")
        user = request.POST.get("Username")
        valid = filesfuncs.userexists(saveslist, user)
        if (valid == True):
            create = True
            saveslist = filesfuncs.makenewfile(saveslist, user)
            return render(request, 'createsave.html', {"saves": saveslist, "error": error,  "create": create, "user": ""})
        else:
            error = True
            return render(request, 'createsave.html', {"saves": saveslist, "error": error,  "create": create, "user": user})

