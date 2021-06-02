# Seraphina Chastity Courtney
# University of New Orleans: Digital Forensics: CSCI 5623 - 20377 
# pypff library credit: joachimmetz
# pypff source: https://github.com/libyal/libpff

# Install pypff prior to use: pip install libpff-python-ratom

from os import lseek
import sys
import pypff
import os
import glob

def parsePST(rootFolder):
    if not os.path.exists('./PST_Output'):
      os.makedirs('./PST_Output')
    for folder in rootFolder.sub_folders:
        currFile = open("./PST_Output/"+str(folder.name)+".txt", "+a")
        currFile.write("Subject|||Sender Name|||Body Text|||Delivery Time\n")
        if folder.number_of_sub_folders:
            parsePST(folder)
        for message in folder.sub_messages:
            currFile.write(
                str(message.subject) + "|||" +
                str(message.sender_name) + "|||" +
                str(message.plain_text_body) + "|||" + 
                str(message.delivery_time) + "\n"                    
            )
        currFile.close()
    return 0  
    
def listFolders(output):
    folders = glob.glob("./PST_Output/*.txt")
    items = []
    for folder in folders:
        folderName = folder.split("\\")[1].split(".")[0]
        currFile = "./PST_Output/"+str(folderName)+".txt"
        with open(currFile) as f:
            for i, l in enumerate(f):
                pass
        lineCount = i + 1
        if output == True:
            print(folderName + "[" + str(lineCount) + "]")
        items.append(folderName + "[" + str(lineCount) + "]")
    return items
    
def listSenderSubject():
    folders = listFolders(False)
    menuCount = 0
    menuChoice1 = -1
    messages = []
    lineCount = 0
    while menuChoice1 != 0:
        print("---------------------\n(0)EXIT\n")
        menuCount = 0
        for folder in folders:
            menuCount += 1
            print("("+str(menuCount)+") "+ folder)
        print("---------------------\n")
        menuChoice1 = int(input("Select Folder: "))
        if menuChoice1 != 0:
        #print(str(folders[menuChoice-1]).split("[")[0]+".txt")
            with open("./PST_Output/"+str(folders[menuChoice1-1]).split("[")[0]+".txt") as dasFolder:
            # print("SUCCESS!")
                print("---------------------\n(0)EXIT\n")
                messages.clear()
                lineCount = 0
                for line in dasFolder:
                    lineCount += 1
                    messages.append(str(line))
                    line = str(line).split("|||")
                    print("("+str(lineCount)+")"+"Delivery Time:"+line[-1]+"SENDER: "+line[1]+ " SUBJECT: " + line[0])
            menuChoice1 = -1
            print("---------------------\n")
            menuChoice1 = int(input("Select Message: "))
            currMessage = str(messages[menuChoice1-1]).split("|||")
            print("Delivery Time:"+currMessage[-1]+"\nSENDER: "+currMessage[1]+ "\nSUBJECT: " + currMessage[0 ]+ "\nBody: \n" + currMessage[2].split("\"")[1])
            menuChoice1 = -1
    return 0

def main():
    menuChoice = -1
    hasParsed = False
    pst = pypff.file()
    while(menuChoice != 0):
        print("---------------------\nDrunk Hermes\n---------------------")
        print(" (1) Parse PST")
        if os.path.exists('./PST_Output'):
            print(" (2) List Folders")
            print(" (3) List Items")
        print(" (0) EXIT")
        print("---------------------")
        menuChoice = int(input())
        if menuChoice == 1:
            pst.open(input("PST Path: "))
            emails = parsePST(pst.get_root_folder())
            hasParsed = True
        elif menuChoice == 2:
            listFolders(True)
        elif menuChoice == 3:
            listSenderSubject()
    pst.close()

if __name__ == "__main__":
  main()