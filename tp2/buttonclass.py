import fileClass



class Button(object):

    def __init__(self,name,width,height,optionNames):
        self.name=name
        self.width=width
        self.height=height
        self.pressed=False
        self.optionNames=optionNames#a list of strings
        self.options=[]
        for i in range(len(self.optionNames)):
            name=self.optionNames[i]
            #i: let it know whcih row it belongs to
            op=Options(name,i,self.height)
            self.options.append(op)
            

    def draw(self,canvas,n):
        x1=n*self.width
        x2=x1+self.width
        y1=0
        y2=self.height
        if self.pressed:
            #change the background color of the button
            canvas.create_rectangle(x1,y1,x2,y2,fill='aliceblue',width=0)
            #and draw options
            canvas.create_rectangle(x1,y2,x1+90,y2+self.height*len(self.optionNames),fill='skyblue',width=0)
            '''for i in range (len(self.optionNames)):
                left=x1
                right=x1+90
                top=y2+self.height*i
                bottom=y2+self.height*(i+1)
                name=self.optionNames[i]
                name=' '+name
                canvas.create_text(left,(top+bottom)/2,text=name,anchor='w',
                        fill='darkslategrey',font="Avenir 15")'''
            for op in self.options:
                #x: let the button knows where its parent is
                op.draw(canvas,x1,y2)
        #whether pressed of not, we always need to draw the button
        canvas.create_text((x1+x2)/2,(y1+y2)/2,text=self.name,
                            fill='darkslategrey',font="Avenir 15")
    
    

class Options(object):
    #options class store all the commands like save, etc.
    def __init__(self,name,index,height,length=90):
        self.name=name
        self.index=index
        self.height=height
        self.length=length
        self.pressed=False
        
    def draw(self,canvas,x,y):
        i=self.index
        left=x
        right=x+self.length
        top=y+self.height*i
        bottom=y+self.height*(i+1)
        name=' '+self.name
        if self.pressed==True:
            canvas.create_rectangle(left,top,right,bottom,fill='aliceblue',width=0)
        
        #always have name on top
        canvas.create_text(left,(top+bottom)/2,text=name,anchor='w',
                fill='darkslategrey',font="Avenir 15")
        
    def operateWithCanvas(self,canvas,data):
        #differnt operations should be called inside different functions
        if self.pressed == True:
            if self.name=='CaPS':
                left=0
                top=data.height/4
                right=data.width
                bottom=3*top
                canvas.create_rectangle(left,top,right,bottom,fill='navy')
                contact='412-268-2922\nhttps://www.cmu.edu/counseling/'
                canvas.create_text(data.width/2,data.height/2,text=contact,fill='white')
                
            elif self.name=='Introduction':
                left=0
                top=data.height/4
                right=data.width
                bottom=3*top
                canvas.create_rectangle(left,top,right,bottom,fill='navy')
                intro='Hello!'
                canvas.create_text(data.width/2,data.height/2,text=contact,fill='white')
            
            

            elif self.name=='Open':
                canvas.create_rectangle(0,0,400,300,fill='midnightblue')
                canvas.create_rectangle(10,270,70,290,fill='royalblue',width=0)
                canvas.create_text(40,280,text='Cancel',font="Avenir 15",fill='azure')
                canvas.create_text(55,50,text='Desktop',font="Avenir 12",fill='azure')
                #draw selected path
                for i in range(1,len(data.dList)):
                    x1=10
                    x2=100
                    y1=40+20*i
                    y2=y1+20
                    canvas.create_rectangle(x1,y1,x2,y2,outline='royalblue',width=3)
                    canvas.create_text((x1+x2)/2,(y1+y2)/2,text=data.dList[i].split('/')[-1],font="Avenir 12",fill='azure')
                if data.target==None:
                #draw path choices
                    choiceToShow=data.folderChoices[data.windowRoll:]
                    choiceToShow=choiceToShow[:11]
                    
                    for i in range(len(choiceToShow)):
                        file=choiceToShow[i]
                        a=file.split('/')
                        name=a[-1]
                        y=50+i*20
                        x=120
                        canvas.create_text(x,y,text=name,font="Avenir 12",fill='azure',anchor='w')
                    canvas.create_text(55,10,text=data.name,anchor='nw',font="Avenir 15",fill='azure')
                else:
                    #draw file preview
                    canvas.create_text(120,50,text=data.targetContent,anchor='nw',font="Avenir 10",fill='azure')
                canvas.create_rectangle(355,40,400,300,fill='midnightblue',width=0)
                canvas.create_rectangle(100,260,400,300,fill='midnightblue',width=0)
                canvas.create_polygon(360,150,390,150,375,120,fill='royalblue',width=0)
                canvas.create_polygon(360,150,390,150,375,180,fill='royalblue',width=0)
                canvas.create_line(360,150,390,150,fill='midnightblue',width=4)
                canvas.create_rectangle(335,270,395,290,fill='royalblue',width=0)
                canvas.create_rectangle(10,40,100,60,outline='royalblue',width=3)
                canvas.create_rectangle(100,40,390,260,outline='royalblue',width=3)
                canvas.create_text(365,280,text='Open',font="Avenir 15",fill='azure')
                    
            elif self.name=='Save':
                #only do this if it does not have a name!!
                canvas.create_rectangle(0,0,400,300,fill='midnightblue')
                canvas.create_rectangle(52,10,390,30,fill='royalblue',width=0)
                canvas.create_text(10,10,text='Name',anchor='nw',font="Avenir 15",fill='azure')
                canvas.create_rectangle(335,270,395,290,fill='royalblue',width=0)
                canvas.create_text(365,280,text='Save',font="Avenir 15",fill='azure')
                canvas.create_rectangle(10,270,70,290,fill='royalblue',width=0)
                canvas.create_text(40,280,text='Cancel',font="Avenir 15",fill='azure')
                canvas.create_rectangle(10,40,100,60,outline='royalblue',width=3)
                canvas.create_text(55,50,text='Desktop',font="Avenir 12",fill='azure')
                #draw selected path
                for i in range(1,len(data.dList)):
                    x1=10
                    x2=100
                    y1=40+20*i
                    y2=y1+20
                    canvas.create_rectangle(x1,y1,x2,y2,outline='royalblue',width=3)
                    canvas.create_text((x1+x2)/2,(y1+y2)/2,text=data.dList[i].split('/')[-1],font="Avenir 12",fill='azure')
                #draw path choices
                canvas.create_rectangle(100,40,390,260,outline='royalblue',width=3)
                for i in range(len(data.folderChoices)):
                    file=data.folderChoices[i]
                    a=file.split('/')
                    name=a[-1]
                    y=50+i*20
                    x=120
                    canvas.create_text(x,y,text=name,font="Avenir 12",fill='azure',anchor='w')
                canvas.create_text(55,10,text=data.name,anchor='nw',font="Avenir 15",fill='azure')
    
    def operateWithoutCanvas(self,data):
        
        def findSpaces(s):
            n=0
            for c in s:
                if c==' ':
                    n+=1
                else:
                    break
            return n
            
        def findLine(s,n):
            #if s[n]=='\n', it is the last line
            i=0
            lineNum=0
            while i<n:
                c=s[i]
                if c=='\n':
                    lineNum +=1
                i+=1
            if s[n]=='\n':
                lineNum -=1
            return lineNum
            
        if self.pressed == True:
            if self.name=='Zoom in':
                if data.wordSize<50:
                    data.wordSize += 5
                    if data.wordSize <35:
                        h=data.wordSize +1
                    else:
                        h=data.wordSize +2
                    data.cellSize=[data.wordSize*3/5,h]
            elif self.name=='Zoom out':
                if data.wordSize>15:
                    data.wordSize -= 5
                    if data.wordSize<35:
                        h=data.wordSize +1
                    else:
                        h=data.wordSize +2
                    data.cellSize=[data.wordSize*3/5,h]
                    
                    
                    
                    
            elif self.name=='Comment':
                if data.isHighlighting==False:
                    data.lines[data.currLine] = "#"+data.lines[data.currLine]
                    data.cursorIndex+=1
                else:
                    start=findLine(data.text1,data.HLstart)
                    end=findLine(data.text1,data.HLend-1)
                    for i in range(start,end+1):
                        data.lines[i] = "#" +data.lines[i]
                    data.cursorIndex+=end-start+1
                data.text=('\n').join(data.lines)
                data.text1=data.text
                
            elif self.name=='Uncomment':
                if data.isHighlighting==False:
                    if data.lines[data.currLine].startswith('#'):
                        data.lines[data.currLine]=data.lines[data.currLine][1:]
                        data.cursorIndex -=1
                else:
                    start=findLine(data.text1,data.HLstart)
                    end=findLine(data.text1,data.HLend-1)
                    for i in range(start,end+1):
                        if data.lines[i].startswith('#'):
                            data.lines[i]=data.lines[i][1:]
                            data.cursorIndex -=1
                data.text=('\n').join(data.lines)
                data.text1=data.text
                
            elif self.name=='Indent':
                if data.isHighlighting==False:
                    data.lines[data.currLine]='    '+data.lines[data.currLine]
                    data.cursorIndex+=4
                else:
                    start=findLine(data.text1,data.HLstart)
                    end=findLine(data.text1,data.HLend-1)
                    for i in range(start,end+1):
                        data.lines[i]='    '+data.lines[i]
                    data.cursorIndex+=end-start+4
                data.text=('\n').join(data.lines)
                data.text1=data.text
                
            elif self.name=='Dedent':
                if data.isHighlighting==False:
                    n=findSpaces(data.lines[data.currLine])
                    if n>4:
                        data.lines[data.currLine]=data.lines[data.currLine][4:]
                        data.cursorIndex -=4
                    elif n>0:
                        data.lines[data.currLine]=data.lines[data.currLine][n:]
                        data.cursorIndex -=n
                
                else:
                    start=findLine(data.text1,data.HLstart)
                    end=findLine(data.text1,data.HLend-1)
                    for i in range(start,end+1):
                        n=findSpaces(data.lines[data.currLine])
                        if n>4:
                            data.lines[data.currLine]=data.lines[data.currLine][4:]
                            data.cursorIndex -=4
                        elif n>0:
                            data.lines[data.currLine]=data.lines[data.currLine][n:]
                            data.cursorIndex -=n    
                data.text=('\n').join(data.lines)
                data.text1=data.text


            elif self.name=='New':
                tmpCount=0
                for file in data.allFiles:
                    if 'tmp' in file.name:
                        tmpCount +=1
                newF=fileClass.File('tmp'+str(tmpCount),'',data.pathRoot)
                data.allFiles.append(newF)
                data.currFile=data.allFiles[-1]
                data.text=data.currFile.content
                data.text1=data.text
                data.lines=data.text1.splitlines()
                if data.lines==[]:
                    data.lines=['']

                

            
                    

                

                            
