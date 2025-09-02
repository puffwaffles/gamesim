from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import pandas as pd
import json
import os
import filesfuncs

def home(request):
    template = loader.get_template('start.html')
    return HttpResponse(template.render())

