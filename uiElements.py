import pygame
from pygame.locals import *
import scenemanager
import classes
from math import floor

pygame.init()

screenDims = (1280,720)

DEFAULTFONTSIZE = int(screenDims[1]/(360/50))
DEFAULTFONT = pygame.font.SysFont(None,DEFAULTFONTSIZE)
NAMEFONTSIZE = int(screenDims[1]/(360/20))
NAMEFONT = pygame.font.SysFont(None,NAMEFONTSIZE)

BACKGROUNDCOLOR = pygame.Color(80,158,40)
BACKGROUND = pygame.surface.Surface(screenDims).fill(BACKGROUNDCOLOR)
HPBACKGROUNDCOLOR = pygame.Color(180,180,180)
HPFOREGROUNDCOLOR = pygame.Color(180,0,0)
MOVESELECTBACKGROUNDCOLOR = pygame.Color(200,200,200)
MOVESELECTFOREGROUNDCOLOR = pygame.Color(240,240,240)
BUTTONHOVERCOLOR = pygame.Color(200,200,255)
BUTTONPRESSCOLOR = pygame.Color(160,160,225)

TESTCOLOR = pygame.Color(255,0,255)

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
        return

class Box:
    def __init__(self,relrect,parent,color = pygame.Color("white"),border_radius = 0, margin = Margin(0,0,0,0), children = [None]):
        self.relrect = relrect
        self.color = color
        self.border_radius = border_radius
        if parent == None:
            self.parent = None
        else:
            self.setparent(parent)
        self.children = children
        self.margin = margin
        self.absrect = self.calcabsrect()
        return

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.absrect, border_radius = self.border_radius)
        return

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
        return

    def addchild(self,child):
        self.children.append(child)
        return
    
    def removechild(self,child):
        #this function sounds so ominous
        for i,x in enumerate(self.children):
            if (x == child):
                x.parent = None
                self.children.pop(i)
        return

    def setparent(self,parent):
        self.parent = parent
        self.parent.addchild(self)
        self.absrect = self.calcabsrect()
        return


class Button:
    def __init__(self,name,text,box,font=DEFAULTFONT,textcolor=pygame.Color("white"),backgroundcolor=BACKGROUNDCOLOR,hovercolor=BUTTONHOVERCOLOR,presscolor=BUTTONPRESSCOLOR,border_radius = 7):
        self.text = text
        self.box = box
        self.font = font
        self.textcolor = textcolor
        self.backgroundcolor = backgroundcolor
        self.hovercolor = hovercolor
        self.presscolor = presscolor
        self.border_radius = border_radius
        self.name = name
        return

    def draw(self,surface):
        buttoncolor = self.backgroundcolor
        if (self.collidemouse()):
            if (pygame.mouse.get_pressed(3)[0]):
                buttoncolor = self.presscolor
            else:
                buttoncolor = self.hovercolor
        
        pygame.draw.rect(surface, buttoncolor, self.box.absrect ,border_radius=self.border_radius)
        renderTextAtPos(surface,self.text,self.box.absrect.center,alignment="centre",color = self.textcolor,font = self.font , backgroundcolor=buttoncolor)
        return

    def collidemouse(self):
        if self.box.absrect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

class TextBox:
    def __init__(   
            self,
            box,
            lines,
            font=DEFAULTFONT,
            textcolor=pygame.Color("white"),
            backgroundcolor=BACKGROUNDCOLOR,
            border_radius = 7
        ):
        self.box = box
        if hasattr(lines, '__iter__'): 
            self.lines = []
            for line in lines:
                self.lines.append(str(line))
        else:
            self.lines = [str(lines)]
        self.font = font
        self.textcolor = textcolor
        self.backgroundcolor = backgroundcolor
        self.border_radius = border_radius
        return
    
    def draw(self,surface):
        pygame.draw.rect(surface, self.backgroundcolor, self.box.absrect ,border_radius=self.border_radius)
        
        for linenum,line in enumerate(self.lines):
            textpos = (self.box.absrect.left,linenum*self.font.get_height())
            temp = self.font.render(line,True,self.textcolor)
            surface.blit(temp,(self.box.absrect.left,self.box.absrect.top+linenum*self.font.get_height()))
        return

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
    elif (alignment == "centre"):
        textpos = (pos[0] - textSurface.get_width()/2 , pos[1] - textSurface.get_height()/2)

    backFill = pygame.surface.Surface((textSurface.get_width(),textSurface.get_height()))
    backFill.fill(backgroundcolor)
    surface.blit(backFill,textpos)
    surface.blit(textSurface,textpos)
    return Rect(textpos,(textSurface.get_width(),textSurface.get_height()))