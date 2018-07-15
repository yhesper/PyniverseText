from tkinter import *
import string
import buttonclass
import keyword
import pythonFeatures
import copy
import planetClass
import random
import withOS
import os
import fileClass

###create colors. from https://www.cs.cmu.edu/~112/notes/notes-graphics.html
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)


####barebone https://www.cs.cmu.edu/~112/notes/events-example0.py

def init(data):
    
    #find the desktop's directory
    data.pathRoot=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') #https://stackoverflow.com/questions/34275782/how-to-get-desktop-location-using-python
    data.colors=['lightskyblue','powderblue','paleturquoise']
    data.backgroundColor=rgbString(4,22,58)
    data.fontFamily='Courier'
    #text and text1: the current file
    data.text=''
    data.text1=data.text
    data.lines=['']
    newF=fileClass.File('tmp',data.text,data.pathRoot)
    data.allFiles=[newF]
    data.currFile=data.allFiles[-1]
    #file name=data.currFile.name
    
    
    data.wordSize=15
    data.menuHeight=30
    data.menuWidth=data.width
    data.cellSize=[9,16]
    
    #draw animation
    data.lastBound=(40,30,40,30+data.cellSize[1])
    data.speed=5
    data.planetList=[]
    data.colorMap=[]
    
    #cursor and highlight
    data.mouseX1=None
    data.mouseY1=None
    data.mouseX2=None
    data.mouseY2=None
    data.isHighlighting=False
    data.HLstart=None#index
    data.HLend=None#index
    data.mouse1justchanged=False
    data.cursorIndex=0
    data.currLine=0
    
    #indention
    data.indention=0#a number store how many 
    #parenthesis
    #check if they are balanced. if not,draw a short line below it
    #def 
    data.round=0
    data.box=0
    data.curly=0
    data.angle=0
    
    #buttons
    #these two let us know which button is pressed
    data.pressedIndex=None
    data.pressedOperation=None
    data.buttonwidth=50
    fileButton=buttonclass.Button('File',data.buttonwidth,data.menuHeight,['New','Open','Save'])
    editButton=buttonclass.Button('Edit',data.buttonwidth,data.menuHeight, ['Undo','Redo','Copy','Paste','Indent','Dedent','Comment','Uncomment'])
    viewButton=buttonclass.Button('View',data.buttonwidth,data.menuHeight,['Zoom in','Zoom out'])
    helpButton=buttonclass.Button('Help',data.buttonwidth,data.menuHeight,['Introduction','CaPS'])
    data.buttons=[fileButton,editButton,viewButton,helpButton]
    data.windowOpen=False
    #only one button can be true in the moment
    
    #file
    
    data.destination=data.pathRoot
    data.dList=['DeskTop']
    data.dDict={'DeskTop':'/Users/yh/Desktop'}
    data.folderChoices=withOS.makeFolderChoices(data.destination)#change this whenever destination is changed
    data.name=''
    data.open=False
    data.targetContent=''
    data.target=None#if i click another folder, set target to none again
    data.windowRoll=0
    




def mousePressed(event, data):
    print(data.HLstart,data.HLend)
    # use event.x and event.y
    #if you press a button,it unfold its menu.
    #Click else where,the menu is folded
    if data.open==True:
        if data.pressedOperation==2:
            withOS.saveMouse(event.x,event.y,data)
        elif data.pressedOperation==1:
            withOS.openMouse(event.x,event.y,data)
            
    else:
        aboutFile(event.x,event.y,data)
        aboutButtons(event.x,event.y,data)
        if event.y>data.menuHeight and event.y< data.height\
        and event.x>0 and event.x<data.width and data.windowOpen==False:
            if event.x!=data.mouseX1 or event.y != data.mouseY1:
                data.mouseX2=None
                data.mouseY2=None
                data.isHighlighting=False
                data.HLstart=None
                data.HLend=None
            data.mouseX1=event.x
            data.mouseY1=event.y
            data.mouse1justchanged=True
            createPlanet(data,event.x,event.y,6)

    

def mouseDragging(event,data):
    data.mouseX2=event.x
    data.mouseY2=event.y

def aboutFile(x,y,data):
    data.currFile.content=data.text
    maxY=data.menuHeight+20*len(data.allFiles)
    if x>0 and x< 110 and y>data.menuHeight and y<maxY:
        i=(y-data.menuHeight)//20
        data.currFile=data.allFiles[i]
        data.text=data.currFile.content
        data.text1=data.text
        data.lines=data.text.splitlines()
        if data.lines==[]:
            data.lines=['']
        
def aboutButtons(x,y,data):
    if data.pressedIndex == None:
        if y>0 and y<data.menuHeight:
            n=x//data.buttonwidth
            if n<len(data.buttons):
                #identify which button you are clicking 
                #make sure index is not out of range
                data.pressedIndex=n
                data.buttons[n].pressed=True#the we may call the different drawfunction
    else:
        currButton=data.buttons[data.pressedIndex]
        currOptions=currButton.options#a list of string
        if not (x>data.buttonwidth*data.pressedIndex and \
        x<data.pressedIndex*data.buttonwidth+70 and \
        y> data.menuHeight and  \
        y< data.menuHeight+currButton.height*len(currOptions)):
            data.buttons[data.pressedIndex].pressed=False
            if data.pressedOperation !=None:
                data.buttons[data.pressedIndex].options[data.pressedOperation].pressed=False
            data.pressedIndex=None
            data.pressedOperation=None
            
        else:
            if data.pressedOperation !=None:
                data.buttons[data.pressedIndex].options[data.pressedOperation].pressed=False
            i=(y-data.menuHeight)//currButton.height
            currOp=currButton.options[i]#an option object
            currOp.pressed=True
            data.pressedOperation=i
            #differnt operations should be called inside different functions
            #except for help,every option only modify data
            if data.pressedIndex==0 and (data.pressedOperation==1 or data.pressedOperation==2):
                data.open=True
                if data.pressedOperation==2:
                    data.folderChoices=withOS.makeFolderChoices(data.destination)
                elif data.pressedOperation==1:
                    data.folderChoices=withOS.makePathChoices(data.destination)
            if data.pressedIndex!=3 and not (data.pressedIndex==0 and (data.pressedOperation==1 or data.pressedOperation==2)):
                data.buttons[data.pressedIndex].options[data.pressedOperation].operateWithoutCanvas(data)
                #after one operation, set all unpress this button
                data.buttons[data.pressedIndex].pressed=False
                data.buttons[data.pressedIndex].options[data.pressedOperation].pressed=False
                data.pressedOperation=None
                data.pressedIndex=None

def stopHighlight(data):
    data.isHighlighting=False
    data.mouseX2=None
    data.mouseY2=None
    data.HLstart=None
    data.HLend=None

#find the space before other characters
def findSpaces(s):
    n=0
    for c in s:
        if c==' ':
            n+=1
        else:
            break
    return n


def findcurrLine(data):
    n=0
    for c in data.text:
        if c=='\n':
            n+=1
    if data.text1!='' and data.text1[-1]=='\n':
        n -= 1
    data.currLine=max(n,0)
    




def findLastWord(data):
    line=data.lines[data.currLine]
    wordList=pythonFeatures.seperateWords(line)
    last=wordList[-1]#at least one str
    right=150+data.cellSize[0]*len(line)
    top=data.menuHeight+data.cellSize[1]*data.currLine
    bottom=top+data.cellSize[1]
    left=right-data.cellSize[0]*len(last)
    return left,top,right,bottom,data.cellSize[0]*len(last),last
    
#return a boolean value : the new planet is created or not
def createPlanet(data,x,y,r):
    lSquare=(data.width-x)**2+(y-data.menuHeight)**2
    newPlanet=planetClass.Planet(x,y,r,lSquare)
    newColor=random.choice(data.colors)
    guess=newPlanet in data.planetList
    if guess==False:
        data.colorMap.append(newColor)
        data.planetList.append(newPlanet)
    return guess
    
def drawPlanet(canvas,data):
    for i in range(len(data.planetList)):
        currP= data.planetList[i]
        currColor=data.colorMap[i]
        currP.draw(canvas,data,i)

#with cursorIndex, find its x1,y1,x2,y2
def findCurrWord(data):
    line=data.lines[data.currLine]
    wordList=pythonFeatures.seperateWords(line)
    last=data.text1[data.cursorIndex-1]
    next=data.text1[min(data.cursorIndex,len(data.text1))]
   
   
'''in keypressed,modify data.text then change data.lines,
this makes drawing code easier'''
def keyPressed(event, data):
    data.currFile.modified=True
    if data.open==True and data.pressedOperation==2:
        withOS.saveKey(data,event.keysym)
        return
    '''create new planets'''
    print(data.cursorIndex)
    if data.windowOpen==True:
        return 
    if event.char==' ' or event.char=='\r' or event.char=='\t':#and a newWord is formed
        #note that when \n is pressed, currLine is not updated
        #find last word before changing the text
        x1,y1,x2,y2,l,lastword=findLastWord(data)
        if not pythonFeatures.formedBySpace(lastword):
            x=(x1+x2)/2
            y=(y1+y2)/2
            r=l/2
            r=r/3
            lSquare=(data.width-x)**2 + (y-data.menuHeight)**2
            newP=planetClass.Planet(x,y,r,lSquare)
            newColor=random.choice(data.colors)
            if newP in data.planetList:
                planetIndex=data.planetList.index(newP)
                data.planetList[planetIndex].speed= abs(data.planetList[planetIndex].speed)
            else:
                data.planetList.append(newP)
                data.colorMap.append(newColor)
                
    
    elif data.cursorIndex!='-1' and data.cursorIndex!=len(data.text1)-1:
        '''
        #if is backspace, reverse the motion.
        if event.keysym=='BackSpace' and \
        data.text1[max(data.cursorIndex-1,0)] not in string.whitespace :
            result==findCurrWord(data)
            if result!= None:
                x1,y1,x2,y2,l,currword=result[0],result[1],result[2],result[3],result[4],result[5]
                x=(x1+x2)/2
                y=(y1+y2)/2
                r=l/2
                r=r/3
                lSquare=(data.width-x)**2 + (y-data.menuHeight)**2
                newP=planetClass.Planet(x,y,r,lSquare)
                newColor=random.choice(data.colors)
                if newP in data.planetList:
                    planetIndex=data.planetList.index(newP)
                    data.planetList[planetIndex].speed= (-1) * abs(data.planetList[planetIndex].speed)
                else:
                    data.planetList.append(newP)
                    data.planet[-1].speed=(-1) * abs(data.planetList[-1].speed)
                    data.colorMap.append(newColor)'''
        
    if event.keysym=='Caps_Lock':
        pass
    elif event.char in string.printable and event.keysym!='??':
        #first remove highlight
        if data.isHighlighting==True:
            selectedLen=data.HLend-data.HLstart-1
            data.text=data.text[:data.HLstart+1]+data.text[data.HLend+1:]
            data.text1=data.text1[:data.HLstart+1]+data.text1[data.HLend+1:]
            data.cursorIndex=data.cursorIndex-1-selectedLen
            stopHighlight(data)
        #differnt keys
        if event.char=='\t':
            data.indention +=1
            data.text=data.text[:data.cursorIndex]+'    '+data.text[data.cursorIndex:]
            data.text1=data.text1[:data.cursorIndex]+'    '+data.text1[data.cursorIndex:]
            data.cursorIndex+=4
        
        #match paranthesis
        elif event.char=='(':
            data.text=data.text[:data.cursorIndex]+'()'+data.text[data.cursorIndex:]
            data.text1=data.text1[:data.cursorIndex]+'()'+data.text1[data.cursorIndex:]
            data.cursorIndex+=1
            data.round +=1
        elif event.char==')':
            if data.round >0:
                data.cursorIndex+=1
                data.round -=1
            else:
                data.text=data.text[:data.cursorIndex]+')'+data.text[data.cursorIndex:]
                data.text1=data.text1[:data.cursorIndex]+')'+data.text1[data.cursorIndex:]
                data.cursorIndex+=1
                data.round -=1
                
        elif event.char=='[':
            data.text=data.text[:data.cursorIndex]+'[]'+data.text[data.cursorIndex:]
            data.text1=data.text1[:data.cursorIndex]+'[]'+data.text1[data.cursorIndex:]
            data.cursorIndex+=1
            data.box +=1
        elif event.char==']':
            if data.box >0:
                data.cursorIndex+=1
                data.box -=1
            else:
                data.text=data.text[:data.cursorIndex]+']'+data.text[data.cursorIndex:]
                data.text1=data.text1[:data.cursorIndex]+']'+data.text1[data.cursorIndex:]
                data.cursorIndex+=1
                data.box -=1
                
        elif event.char=='{':
            data.text=data.text[:data.cursorIndex]+'{}'+data.text[data.cursorIndex:]
            data.text1=data.text1[:data.cursorIndex]+'{}'+data.text1[data.cursorIndex:]
            data.cursorIndex+=1
            data.curly +=1
        elif event.char=='}':
            if data.curly >0:
                data.cursorIndex+=1
                data.curly -=1
            else:
                data.text=data.text[:data.cursorIndex]+'}'+data.text[data.cursorIndex:]
                data.text1=data.text1[:data.cursorIndex]+'}'+data.text1[data.cursorIndex:]
                data.cursorIndex+=1
                data.curly -=1
                
        elif event.char=='<':
            data.text=data.text[:data.cursorIndex]+'<>'+data.text[data.cursorIndex:]
            data.text1=data.text1[:data.cursorIndex]+'<>'+data.text1[data.cursorIndex:]
            data.cursorIndex+=1
            data.angle +=1
        elif event.char=='>':
            if data.angle >0:
                data.cursorIndex+=1
                data.angle -=1
            else:
                data.text=data.text[:data.cursorIndex]+'>'+data.text[data.cursorIndex:]
                data.text1=data.text1[:data.cursorIndex]+'>'+data.text1[data.cursorIndex:]
                data.cursorIndex+=1
                data.angle -=1
                
        elif event.char != '\r':
            #pay attention to spaces and tabs
            #prevLine=[data,lines[-1]]
            data.text=data.text[:data.cursorIndex]+event.char+data.text[data.cursorIndex:]
            data.text1=data.text1[:data.cursorIndex]+event.char+data.text1[data.cursorIndex:]
            data.cursorIndex+=1
        #press return
        else:
            '''there are two cases:
            if prevLine only has space, follow the number of space
            else follow data.indention'''
            prevLine=data.lines[-1]
            spaces=findSpaces(prevLine)
            if data.lines!=[] and data.text1!='' and data.text!='':
                #check if need new indention
                print(data.cursorIndex)
                
                print(repr(data.text1))
                print(repr(data.text1[-1]))
                edgeIndex=max(data.cursorIndex-1,0)
                if edgeIndex> len(data.text1):
                    edgeIndex=-1
                edgeChar=data.text1[edgeIndex]
                if edgeChar==':':
                    spaces +=4
            data.text=data.text[:data.cursorIndex]+'\n'+' '*spaces+data.text[data.cursorIndex:]
            data.text1=data.text1[:data.cursorIndex]+'\n'+' '*spaces+data.text1[data.cursorIndex:]
            data.cursorIndex=data.cursorIndex+1+spaces
            
    # event.keysym is not printable
    if event.keysym == 'BackSpace':
        selectedLen=0
        if data.isHighlighting==True:
            selectedLen=data.HLend-data.HLstart-1
            data.text=data.text[:data.HLstart]+data.text[data.HLend:]
            data.text1=data.text1[:data.HLstart]+data.text1[data.HLend:]
            stopHighlight(data)
            
        if data.cursorIndex>0:
            data.text=data.text[:data.cursorIndex-1]+data.text[data.cursorIndex:]
            data.text1=data.text1[:data.cursorIndex-1]+data.text1[data.cursorIndex:]
            data.cursorIndex=data.cursorIndex-1-selectedLen
            
    if data.text!='' and data.text1!='':
        data.lines=data.text1.splitlines()
    else:
        data.lines=['']
    #after typing each word, update currLine
    findcurrLine(data)
    if len(data.lines[data.currLine])*data.cellSize[0]+6 +9 > data.width:
        data.text1= data.text1[:-1]+'\n'+data.text1[-1]
        data.lines=data.text1.splitlines()
        data.currLine += 1
        data.cursorIndex += 1
    if data.text!='' and data.text1!='':
        if data.text1[-1]=='\n':
            data.lines.append('')

    print(repr(data.text1))


    

def changeSize(event,data):
    data.height=event.height
    data.width=event.width
    #print(data.width,data.height)
    data.text1=data.text
    

def timerFired(data):
    newList=[]
    for planet in data.planetList:
        planet.move(data)
        if planet.x-planet.r*2<data.width and planet.y-planet.r/2<data.height:
            newList.append(planet)
    data.planetList=newList
        


def drawMenu(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.menuHeight,fill='skyblue',width=0)
    for i in range(len(data.buttons)):
        button=data.buttons[i]
        button.draw(canvas,i)
    #draw the currently selected option
    canvas.create_oval(data.width-30,30-30,data.width+30,30+30,fill='white',width=0)
    canvas.create_oval(data.width-60,30-25,data.width+60,30+25,outline='white',width=2)
    canvas.create_oval(data.width-50,30-17.5,data.width+50,30+17.5,outline='white',width=2)


def drawWritingArea(canvas,data):
    canvas.create_rectangle(0,data.menuHeight,data.width,data.height,fill=data.backgroundColor,width=0)
    
def drawContent(canvas,data):
    myFont=data.fontFamily+' '+str(data.wordSize)
    content=canvas.create_text(150,data.menuHeight,anchor='nw',text=data.text1,fill='darkslategrey',font=myFont)
    #set the focus on content to manage cursor
    canvas.focus_set()
    canvas.focus(content)
    if data.mouse1justchanged==True:
        i=canvas.index(content,'@'+str(data.mouseX1)+','+str(data.mouseY1))
        data.cursorIndex=i
        data.mouse1justchanged=False
    canvas.icursor(content,data.cursorIndex)
    if data.mouseX1!=None and data.mouseY1!=None:
        if data.mouseX2!=None and data.mouseY2!=None:
            j=canvas.index(content,'@'+str(data.mouseX2)+','+str(data.mouseY2))
            smallerIndex=min(data.cursorIndex,j)
            biggerIndex=max(data.cursorIndex,j)
            canvas.select_from(content,smallerIndex)
            canvas.select_to(content,biggerIndex-1)
            data.isHighlighting=True
            data.HLstart=smallerIndex
            data.HLend=biggerIndex
    
    '''value=(canvas.bbox(content))
    #print(value)
    rowHeight=value[3]-value[1]
    print(rowHeight)
    rowLen=value[2]-value[0]
    if rowLen+20>data.width:
        data.text1=data.text1[:-1]+'\n'+data.text1[-1]
    if data.cellSize==None:#you need to deal with this if zoom in or zoom out
        data.cellSize=rowHeight'''
    rows= data.height//data.cellSize[1]
    
    for row in range (rows):
        x1=0
        y1=data.menuHeight+row*data.cellSize[1]
        x2=data.width
        y2=y1+data.cellSize[1]
        #canvas.create_line(x1,y1,x2,y1)
        if row<len(data.lines):
            if row==data.currLine:
                if data.text1!='' and data.text1[-1]=='\n':
                    canvas.create_rectangle(120,y2+3,140,y2+data.cellSize[1],fill='skyblue',width=0)
                else:
                    canvas.create_rectangle(120,y1+3,140,y2,fill='skyblue',width=0)
            canvas.create_text(130,(y1+y2)/2,text=str(row+1),fill='darkslategrey')
    
    
def drawCode(canvas,data):
    lines=data.lines
    #nw 5 data.menuHeight
    drawLine(canvas,15,data.menuHeight,lines,data)

#comments(one line/ more lines) change color
#function name change color
#recursion: determine if it is in triple quote

def drawLine(canvas,x,y,lineList,data,inTripleQuote=False):
    if len(lineList)==0:
        pass
    else:
        currLine=lineList[0]
        if currLine!='':
            words=pythonFeatures.seperateWords(currLine)
            if currLine[0].startswith('#'):
                drawWord(canvas,150,y,words,data,'orange')
                
            else:
                drawWord(canvas,150,y,words,data,'gold')
                
        newLineList=copy.copy(lineList)[1:]
        #indicate the indention
        indentNum=findSpaces(currLine)//4
        canvas.create_line(150+data.cellSize[0]*indentNum*4,y,150+data.cellSize[0]*indentNum*4,y+data.cellSize[1],fill='steelblue')
        drawLine(canvas,150,y+data.cellSize[1],newLineList,data)

#the x y is for anchor='nw'
def drawWordOld(canvas,x,y,wordList,data,color,inTripleQuote=False):
    myFont=data.fontFamily+' '+str(data.wordSize)
    if len(wordList)==0:
        pass
    else:
        currWord=wordList[0]
        newWordList=copy.copy(wordList)[1:]
        data.left=x
        data.right=x+data.cellSize[0]*len(currWord)
        data.top=y
        data.bottom=y+data.cellSize[1]
        if pythonFeatures.isPythonKeyword(currWord):
            myFont=myFont+' '+'bold'
        aWord=canvas.create_text(x,y,text=currWord,anchor='nw',font=myFont,fill=color)
        newX=x+data.cellSize[0]*len(currWord)
        newY=y
        drawWord(canvas,newX,newY,newWordList,data,color)

def drawWord(canvas,x,y,wordList,data,color):
    myFont=data.fontFamily+' '+str(data.wordSize)
    for i in range(len(wordList)):
        myFont=data.fontFamily+' '+str(data.wordSize)
        currWord=wordList[i]
        if pythonFeatures.isPythonKeyword(currWord):
            myFont=myFont+' '+'bold'
        canvas.create_text(x,y,text=currWord,anchor='nw',font=myFont,fill=color)
        x=x+data.cellSize[0]*len(currWord)
        y=y


def drawSidebar(canvas,data):
    canvas.create_rectangle(110,0,150,data.height,fill='steelblue',width=0)

def drawFileName(canvas,data):
    canvas.create_rectangle(0,data.menuHeight,110,data.height,fill='azure',width=0)    
    for i in range(len(data.allFiles)):
        f=data.allFiles[i]
        name=f.name
        y1=data.menuHeight+20*i
        y2=y1+20
        if name== data.currFile.name:
            canvas.create_rectangle(0,y1,110,y2,fill='steelblue',width=0)
        canvas.create_text(55,(y1+y2)/2,text=name,fill='darkslategrey',font="Avenir 15")
    

    
def redrawAll(canvas, data):
    #print(data.cursorIndex)
    # draw in canvas
    myFont=data.fontFamily+' '+str(data.wordSize)
    drawWritingArea(canvas,data)
    drawSidebar(canvas,data)
    drawPlanet(canvas,data)
    drawContent(canvas,data)
    drawCode(canvas,data)
    drawFileName(canvas,data)
    drawMenu(canvas,data)
    if (data.pressedIndex==3 and data.pressedOperation != None)\
    or (data.pressedIndex==0 and (data.pressedOperation ==1 or  data.pressedOperation ==2) and data.open==True):
        data.buttons[data.pressedIndex].options[data.pressedOperation].operateWithCanvas(canvas,data)
    
    #print(data.lines,data.currLine)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
        
    def mouseDraggingWrapper(event, canvas, data):
        mouseDragging(event,data)
        redrawAllWrapper(canvas, data)
        
    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    
    def changeSizeWrapper(event,canvas, data):
        changeSize(event,data)
        redrawAllWrapper(canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1 # milliseconds
    init(data)

    
    # create the root and the canvas and scrollbar

    # set scroll bar
    root = Tk()
    canvas = Canvas(root, width=data.width,height=data.height,insertbackground='yellow',scrollregion=(0, 0,data.width, data.height))

    canvas.pack(side='right',fill='both',expand=True)

    
    
    # set up events
    canvas.bind("<Configure>", lambda event:
                                changeSizeWrapper(event,canvas, data))
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event:
                            mouseDraggingWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app

    root.mainloop()  # blocks until window is closed
    
    print("bye!")

run(1000,500)
