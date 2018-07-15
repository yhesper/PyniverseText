
import math

#################################################
# Helper functions
#################################################



import random

class Planet(object):
    def __init__(self,x,y,r,l2):
        #x and y may changes
        self.x=x
        self.y=y+15
        #r , l and never changes
        self.r=r
        self.l2=l2# l is the square of distance 
        #speed may changes
        self.speed=1
        self.num=random.randint(0,1)
    def __eq__(self,other):
        return isinstance(other,Planet) and abs(self.l2-other.l2)<8
        
    def move(self,data):
        dx=self.speed*self.y/(self.l2)**0.5
        dy=self.speed*(data.width-self.x)/(self.l2)**0.5
        self.x += dx
        self.y += dy
    def __hash__(self):
        return hash(self.l2)
    #different stars
    #def s0(self,canvas,data)
    #def s1(self,canvas,data)
    
    #def m0(self,canvas,data)
    #def m1(self,canvas,data)
    
    #def l0(self,canvas,data)
    #def l1(self,canvas,data)
    
    
    #s=[s0,s1]#character length 0-4
    #m=[m0,m1]#character length 5-10
    #l=[l0,l1]#11 or more
    
    def draw(self,canvas,data,i):
        mycolor=data.colorMap[i]
        if self.x-self.r*2<data.width and self.y-self.r/2<data.height :
            l=((self.y-data.menuHeight)**2+(data.width-self.x)**2)**0.5
            canvas.create_oval(data.width-l,data.menuHeight-l,data.width+l,data.menuHeight+l,outline='steelblue')
            canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill=mycolor,width=0)
            canvas.create_oval(self.x-self.r*2,self.y-self.r/2,self.x+self.r*2,self.y+self.r/2,width=self.r/8,outline=mycolor)
            rSmall=self.r/4
            xSmall=self.x+self.r*3/2
            ySmall=self.y+self.r*3/8
            canvas.create_oval(xSmall-rSmall,ySmall-rSmall,xSmall+rSmall,ySmall+rSmall,fill=mycolor,width=0)
        
            
