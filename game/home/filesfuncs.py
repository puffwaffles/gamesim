import json
import os, os.path

#Acquire contents of files in jsons files directory
def acquirefiles():
    path = r'save files'
    saveslist = {}
    #Iterate through files in save files folder
    for files in os.listdir(path):
        #Check for legitimate save files to add to saveslist
        if (files.endswith(".json")):
            currfile = path + "/" + files
            with open(currfile, "r")  as file: 
                saveslist[files] = json.load(file)
    return saveslist

# Displays save files (excluding file extension)
def displayfiles(saveslist):
    if (len(saveslist) == 0):
        print("No existing save files") 
    else:
        print("Existing saves: ")
        for saves in sorted(saveslist.keys()):
            print(saves[:-5])
    print("\n")
    pass


#Create a new file
def createnewfile(saveslist):
    #Set maximum saves allowed to 5
    if (len(saveslist) > 4):
        print("Maximum number of save files exceeded!")
        print("\n")
        return saveslist
    #Allow for adding a save if limit not exceeded
    else:
        #Use highest existing number for save to ensure no duplicate save files
        highest = 0
        for names in saveslist:
            trunc = names[4:-5]
            if (int(trunc) > highest):
                highest = int(trunc)
        highest = highest + 1
        newfilename = "save " + str(highest) + ".json"
        valid = False
        #Prompt user for username that is not taken by other existing saves
        while (valid == False):
            username = input('Please enter a new username: ')
            valid = True
            for saves in saveslist.values():
                if (saves["Username"] == username):
                    print(f"Error: username \"{username}\" is already taken")
                    print("\n")
                    valid = False
                    break
        
        print("\n")
             
        newcontents = {
            "Username": username,
            "Level": 1,
            "Coins": 100000,
            "Jewels": 500,
            "Inventory": {},
            "Inventory Max Size": 10
        }
        #Update new saves list
        newsaveslist = saveslist
        newsaveslist[newfilename] = newcontents
        
        #Create new file in folder
        newfile = json.dumps(newcontents, indent = 2)
        path = r'save files/'
        newpath = path + newfilename
        with open(newpath, "w") as file:
            file.write(newfile)
        displayfiles(newsaveslist)
        return newsaveslist
    
#Deletes save files
def deletefile(saveslist):
    numsaves = len(saveslist)
    #Allows for file deletion if files exist
    if (numsaves == 0):
        print("No saves available to delete")
        print("\n")
        return saveslist
    else:
        path = r'save files/'
        newsaveslist = saveslist
        displayfiles(saveslist)
        finish = False
        #Prompts user for a save file to be deleted
        while(finish == False):
            #Automatically deletes savefile if only 1 exists
            if (numsaves == 1):
                print("Deleting savefile")
                newsaveslist.clear()
                print(f"Successfully deleted save file")
                print("\n")
                finish = True
            #Prompts user for save file by name
            else:
                choice = input("Please select a save file to delete (i.e. save 1): ")
                if (choice + ".json" not in newsaveslist):
                    print(f"Error: Save file {choice} does not exist")
                    print("\n")
                else:
                    filename = choice + ".json"
                    #Update savefile list
                    del newsaveslist[filename]
                    newpath = path + filename
                    #Remove save file from folder
                    os.remove(newpath)
                    print(f"Successfully deleted {choice}")
                    print("\n")
                    finish = True
        return newsaveslist

#Displays menu options for save file
def filemenudisplay():
    print("1. Display save files")
    print("2. Create new file")
    print("3. Delete old file")
    print("4. Exit")
    print("\n")
    choice = input("Please select 1 of the following options: ")
    print("\n")
    return choice

#Provides menu operations for save files
def filemenu():
    saveslist = acquirefiles()
    finish = False
    print("\n")
    while(finish == False):
        choice = filemenudisplay()
        match choice:
            case "1":
                displayfiles(saveslist) 
            case "2":
                saveslist = createnewfile(saveslist)
            case "3":
                saveslist = deletefile(saveslist)
            case "4":
                finish = True
            case _:
                print("Invalid choice")
                print("\n")
    pass

#Summon menu
filemenu()