import pygame
from pygame.locals import *
from math import floor
import scenemanager
import classes
from globalconstants import *

pygame.init()

DEFAULTFONTSIZE = int(screenDims[1]/7.2)
DEFAULTFONT = pygame.font.SysFont(None,DEFAULTFONTSIZE)
NAMEFONTSIZE = int(screenDims[1]*1/25)
NAMEFONT = pygame.font.SysFont(None,NAMEFONTSIZE)

class Rect_f:
    def __init__(self,left,top,width,height):
        self.top = top
        self.left = left
        self.width = width
        self.height = height

class Margin:
    def __init__(self,left,right,top,bottom,form="%"):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.form = form

class Box:
    def __init__(self,relrect,parent,color = pygame.Color("white"),border_radius = 0, margin = Margin(0,0,0,0), children = [None]):
        self.relrect = relrect #type: Rect_f()
        self.color = color #type: Color()
        self.border_radius = border_radius #type: float
        if parent == None: #type: Box()
            self.parent = None
        else:
            self.setparent(parent)
        self.children = children #type: [Box()]
        self.margin = margin #type: Margin() 
        self.absrect = self.calcabsrect()

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.absrect, border_radius = self.border_radius)

    def calcabsrect(self):
        parent = self.parent
        if (parent == None):
            return None
        else:
            left = self.relrect.left*parent.absrect.width + parent.absrect.left + parent.margin.left*parent.absrect.width
            top = self.relrect.top*parent.absrect.height + parent.absrect.top + parent.margin.top*parent.absrect.height
            width = self.relrect.width*parent.absrect.width*(1-parent.margin.left-parent.margin.right)
            height = self.relrect.height*parent.absrect.height*(1-parent.margin.top-parent.margin.bottom)
            return Rect(left,top,width,height)

    def setrelrect(self,relrect):
        self.relrect = relrect
        self.absrect = self.calcabsrect()

    def addchild(self,child):
        self.children.append(child)
    
    def removechild(self,child):
        #this function sounds so ominous
        for i,x in enumerate(self.children):
            if (x == child):
                x.parent = None
                self.children.pop(i)

    def setparent(self,parent):
        self.parent = parent
        self.parent.addchild(self)
        self.absrect = self.calcabsrect()

class Button:
    def __init__(
            self,
            buttype,
            text,
            box,
            font=DEFAULTFONT,
            textcolor=pygame.Color("white"),
            backgroundcolor=BACKGROUNDCOLOR,
            hovercolor=BUTTONHOVERCOLOR,
            presscolor=BUTTONPRESSCOLOR,
            border_radius = 7,
            action = None,
            actionargs = []
        ):
        self.text = text
        self.box = box
        self.font = font
        self.textcolor = textcolor
        self.backgroundcolor = backgroundcolor
        self.hovercolor = hovercolor
        self.presscolor = presscolor
        self.border_radius = border_radius
        self.type = buttype
        self.action = action
        self.actionargs = actionargs

    def draw(self,surface):
        buttoncolor = self.backgroundcolor
        if (self.collidemouse()):
            if (pygame.mouse.get_pressed(3)[0]):
                buttoncolor = self.presscolor
            else:
                buttoncolor = self.hovercolor
        pygame.draw.rect(surface, buttoncolor, self.box.absrect ,border_radius=self.border_radius)
        renderTextAtPos(surface,self.text,self.box.absrect.center,alignment="centre",color = self.textcolor,font = self.font , backgroundcolor=buttoncolor)
    
    def collidemouse(self):
        if self.box.absrect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False
    
    def setparent(self,parent):
        self.box.setparent(parent)

class TextBox:
    def __init__(   
            self,
            box,
            lines,
            margin=Margin(0,0,0,0),
            font=DEFAULTFONT,
            textcolor=pygame.Color("white"),
            backgroundcolor=BACKGROUNDCOLOR,
            border_radius = 7,
            textalignment = "topLeft"
        ):
        self.box = box
        self.lines = []
        for line in lines:
            self.lines.append(str(line))
        self.font = font
        self.textalignment = textalignment
        self.textcolor = textcolor
        self.backgroundcolor = backgroundcolor
        self.border_radius = border_radius
        self.margin = margin
    
    def draw(self,surface):
        pygame.draw.rect(surface, self.backgroundcolor, self.box.absrect ,border_radius=self.border_radius)
        
        for linenum,line in enumerate(self.lines):
            if (self.textalignment == "topLeft"):
                textpos = ( self.box.absrect.left+self.margin.left*self.box.absrect.width , self.box.absrect.top+linenum*self.font.get_height()+self.margin.top*self.box.absrect.height )
            elif (self.textalignment == "centre"):
                textpos = ( (self.box.absrect.left+self.box.absrect.right)/2 , (self.box.absrect.top+self.box.absrect.bottom)/2-(self.font.get_height()*len(self.lines))/2+(linenum+1)*self.font.get_height()/2 )
            else:
                textpos = ( self.box.absrect.left+self.margin.left*self.box.absrect.width , self.box.absrect.top+linenum*self.font.get_height()+self.margin.top*self.box.absrect.height )
            renderTextAtPos(surface,line,textpos,alignment=self.textalignment,font=self.font,color=self.textcolor,backgroundcolor=self.backgroundcolor)
    
    def setparent(self,parent):
        self.box.setparent(parent)

class Tooltip:
    def __init__(self, text, region = Box(Rect_f(0,0,0.5,0.5),None), ttwidth = 0.5, ttheight = 0.5, font=DEFAULTFONT, bgcolor = pygame.Color("white"), textcolor = pygame.Color("black")):
        text = text
        font = font
        region = region
        bgcolor = bgcolor
        textcolor = textcolor
        width = ttwidth
        height = ttheight

    def collidemouse(self):
        if self.region.absrect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def draw(self, surface):
        if self.collidemouse():
            pygame.draw.rect(surface, self.bgcolor, self.box.absrect ,border_radius=self.box.border_radius)
            renderTextAtPos(surface,self.text,self.box.absrect.topleft,alignment="topLeft",color = self.textcolor,font = self.font , backgroundcolor=self.bgcolor)

def renderTextAtPos(surface,text,pos,alignment="topLeft",font=DEFAULTFONT,color=pygame.Color("white"),backgroundcolor=BACKGROUNDCOLOR):
    textSurface = font.render(text,1,color)
    if (alignment == "topLeft"):
        textpos=pos
    elif (alignment == "topCentre"):
        textpos = (pos[0] - textSurface.get_width()/2, pos[1])
    elif (alignment == "centreLeft"):
        textpos = (pos[0], pos[1] - textSurface.get_height()/2)
    elif (alignment == "centreRight"):
        textpos = (pos[0] - textSurface.get_width(),pos[1] - textSurface.get_height()/2)
    elif (alignment == "topRight"):
        textpos = (pos[0] - textSurface.get_width(),pos[1])
    elif (alignment == "centre"):
        textpos = (pos[0] - textSurface.get_width()/2 , pos[1] - textSurface.get_height()/2)
    else:
        raise Exception("invalid alignment given")

    backFill = pygame.surface.Surface((textSurface.get_width(),textSurface.get_height()))
    backFill.fill(backgroundcolor)
    surface.blit(backFill,textpos)
    surface.blit(textSurface,textpos)
    return Rect(textpos,(textSurface.get_width(),textSurface.get_height()))

BASEBOX = Box(
    relrect = Rect_f(0,0,1,1),
    parent = None
)
BASEBOX.absrect = Rect(0,0,screenDims[0],screenDims[1])

MAJORBOX = Box(
    relrect = Rect_f(0.02,0.55,0.96,0.43),
    color = HPBACKGROUNDCOLOR,
    parent = BASEBOX,
    border_radius = 14,
    margin = Margin(0.005,0.005,0.03,0.03)
)

MINORBOX = Box(
    relrect = Rect_f(0,0,1,1),
    parent=MAJORBOX
)