import os
import string
###save and open both need
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def makePathChoices(path):
    l=[]
    all=os.listdir(path)
    for one in all:
        newPath=path+'/'+one
        l.append(newPath)
    return l


def chooseOldPath(data,x,y):
    i=(y-40)//20
    if i < len(data.dList):
        name=data.dList[i]
        data.destination=data.dDict[name]
        data.folderChoices=makePathChoices(data.destination)
        data.target=None
        data.targetContent=''
        data.dList=data.dList[:i+1]
        for file in data.dList[i+1:]:
            del data.dDict[file]
            
####save

def chooseOldFolder(data,x,y):
    i=(y-40)//20
    if i < len(data.dList):
        name=data.dList[i]
        data.destination=data.dDict[name]
        data.folderChoices=makeFolderChoices(data.destination)
        data.dList=data.dList[:i+1]
        for file in data.dList[i+1:]:
            del data.dDict[file]

def chooseNewPath(data,x,y):
    if y< 40+len(data.folderChoices)*20:
        i=(y-40)//20
        chosenFolder=data.folderChoices[i]#this is a path
        data.destination=chosenFolder
        name=chosenFolder.split('/')[-1]
        data.dList.append(name)
        data.dDict[name]=chosenFolder
        data.folderChoices=makeFolderChoices(chosenFolder)
        
def makeFolderChoices(path):
    l=[]
    all=os.listdir(path)
    for one in all:
        newPath=path+'/'+one
        if os.path.isdir(newPath):
            l.append(newPath)
    return l
    
def saveMouse(x,y,data):
    if x>334 and x< 395 and y>270 and y<290:
        os.chdir(data.destination)
        if 'tmp'in data.name:
            name='newFile.py'
        else:name=data.name+'.py'
        if name in os.listdir(data.destination):
            if name[-4].isdigit():
                name=name[:-4]+str(int(name[-4])+1)+'.py'
            else:
                name=name[:-4]+'1'+'.py'
                
        writeFile(name, data.text)
        data.buttons[data.pressedIndex].pressed=False
        data.buttons[data.pressedIndex].options[data.pressedOperation].pressed=False
        data.open=False
        data.pressedOperation=None
        data.pressedIndex=None
        data.destination=data.pathRoot
        data.dList=['DeskTop']
        data.dDict={'DeskTop':'/Users/yh/Desktop'}
        data.folderChoices=makeFolderChoices(data.destination)
    elif y>10 and y<30 and x>334 and x< 395:
        old=data.destination.split
        new=old[:-1]
        data.destination=new.join('/')
        if len(data.destination) < len(data.pathRoot) :
             data.destination=data.pathRoot
    elif x>100 and x<390 and y>40 and y<260:
        chooseNewPath(data,x,y)
    elif x> 10 and x< 100 and y>40 and y<100:
        chooseOldFolder(data,x,y)
    elif x>10 and x<70 and y>270 and y<290:
        data.buttons[data.pressedIndex].pressed=False
        data.buttons[data.pressedIndex].options[data.pressedOperation].pressed=False
        data.open=False
        data.pressedIndex=None
        data.pressedOperation=None
        data.destination=data.pathRoot
        data.dList=['DeskTop']
        data.dDict={'DeskTop':'/Users/yh/Desktop'}
        data.folderChoices=makeFolderChoices(data.destination)


        
def saveKey(data,sym):
    if sym in string.printable and sym!='??':
        data.name= data.name +sym
    elif sym == 'BackSpace':
        data.name=data.name[:-1]
    
        
####open 


def chooseNewFile(data,x,y):
    if y< 40+len(data.folderChoices)*20:
        i=(y-40)//20
        chosen=data.folderChoices[i]#this is a path
        if os.path.isdir(chosen):
            data.destination=chosen
            name=chosen.split('/')[-1]
            data.dList.append(name)
            data.dDict[name]=chosen
            data.folderChoices=makePathChoices(chosen)
        else:
            try:
                data.target=chosen
                data.targetContent=readFile(chosen)
            except:
                print("Sorry I can't open this.")
            

 


def openMouse(x,y,data):
    if x>334 and x< 395 and y>270 and y<290:
        data.text=data.targetContent
        name=data.target.split('/')[-1]
        newF=fileClass.File(name,data.text,data.target)
        data.allFiles.append(newF)
        data.currFile=data.allFiles[-1]
        data.text=data.currFile.content
        data.text1=data.text
        data.lines=data.text1.splitlines()
        if data.lines==[]:data.lines=['']
        
        data.buttons[data.pressedIndex].pressed=False
        data.buttons[data.pressedIndex].options[data.pressedOperation].pressed=False
        data.open=False
        data.pressedOperation=None
        data.pressedIndex=None
        data.target=None
        data.targetContent=''
        data.windowRoll=0
    elif y>10 and y<30 and x>334 and x< 395:
        old=data.destination.split
        new=old[:-1]
        data.destination=new.join('/')
        if len(data.destination) < len(data.pathRoot) :
             data.destination=data.pathRoot
        
    elif x<390 and x>360 and y>150 and y<180 and len(data.folderChoices)>10:
        data.windowRoll+=1
        if data.windowRoll>len(data.folderChoices)-10:
            data.windowRoll=len(data.folderChoices)-10
    elif x<390 and x> 360 and y< 150 and y>120 and len(data.folderChoices)>10:
        data.windowRoll-=1
        if data.windowRoll<0:
            data.windowRoll=0
    elif x>100 and x<350 and y>40 and y<260:
        y += data.windowRoll*20
        chooseNewFile(data,x,y)
    elif x> 10 and x< 100 and y>40 and y<260:
        chooseOldPath(data,x,y)#this can be used for both save and open
    elif x>10 and x<70 and y>270 and y<290:
        data.buttons[data.pressedIndex].pressed=False
        data.buttons[data.pressedIndex].options[data.pressedOperation].pressed=False
        data.open=False
        data.target=None
        data.targetContent=''
        data.pressedOperation=None
        data.pressedIndex=None
        data.windowRoll=0


