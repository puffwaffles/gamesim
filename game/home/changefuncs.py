import json
import os, os.path
from . import filesfuncs

def maketransaction(username, item, operation, amount):
    success = True
    tempcontents = filesfuncs.gettemp(username)
    savename = tempcontents["Save Name"]

    if (item != "Real Money Spent" and operation != "*"):
        amount = int(amount)
    else:
        amount = round(float(amount), 2)

    match operation:
        case "+":
            tempcontents["Contents"][item] = tempcontents["Contents"][item] + amount
        case "-":
            if (checktransaction(username, item, amount)):
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

    tempfile = filesfuncs.replacetemp(username, tempcontents)

    return success

#Checks if transaction is valid
def checktransaction(username, currency, amount):
    success = False
    tempcontents = filesfuncs.gettemp(username)
    
    if (tempcontents["Contents"][currency] - amount >= 0):
        success = True
    return success