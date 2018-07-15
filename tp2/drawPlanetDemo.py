# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.cx=50
    data.cy=50
    data.r=20
    data.speed=data.r/20
    
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    l=(data.cy**2+(data.width-data.cx)**2)**0.5
    dx=data.speed*data.cy/l
    dy=data.speed*(data.width-data.cx)/l
    data.cx += dx
    data.cy += dy


def redrawAll(canvas, data):
    if data.cx-data.r*2<data.width and data.cy-data.r/2<data.height :
        l=(data.cy**2+(data.width-data.cx)**2)**0.5
        canvas.create_oval(data.width-l,-l,data.width+l,l)
        canvas.create_oval(data.cx-data.r,data.cy-data.r,data.cx+data.r,data.cy+data.r,
            fill='blue',width=0)
        canvas.create_oval(data.cx-data.r*2,data.cy-data.r/2,data.cx+data.r*2,data.cy+data.r/2,width=data.r/8,outline='blue')
        rSmall=data.r/4
        xSmall=data.cx+data.r*3/2
        ySmall=data.cy+data.r*3/8
        canvas.create_oval(xSmall-rSmall,ySmall-rSmall,xSmall+rSmall,ySmall+rSmall,fill='blue',width=0)
    #canvas.create_oval(data.cx-data.r*2,data.cy-data.r*2,data.cx+data.r*2,data.cy+data.r*2,width=data.r/8,outline='blue')
    

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

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600,600)