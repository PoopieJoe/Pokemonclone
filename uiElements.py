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
    def __init__(self, gettext, gettextargs = [], region = Box(Rect_f(0,0,0.5,0.5),None), ttwidth = 0.5, ttheight = 0.5, font=NAMEFONT, bgcolor = pygame.Color("white"), textcolor = pygame.Color("black"),textalignment="topLeft"):
        self.gettext = gettext
        self.gettextargs = gettextargs
        self.font = font
        self.region = region
        self.bgcolor = bgcolor
        self.textcolor = textcolor
        self.width = ttwidth
        self.height = ttheight
        self.textalignment = textalignment

    def collidemouse(self):
        if self.region.absrect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def draw(self, surface):
        if self.collidemouse():
            #update tooltip text
            self.text = self.gettext(*(self.gettextargs))
            lenlist = [len(line) for line in self.text]
            longestline = self.text[lenlist.index(max(lenlist))]
            (boxwidth,_) = self.font.size(longestline)
            boxheight = len(self.text)*self.font.get_height()

            (absx,absy) = pygame.mouse.get_pos()

            ttbox = Box(Rect_f(absx/screenDims[0],absy/screenDims[1],boxwidth/screenDims[0],boxheight/screenDims[1]),BASEBOX)
            pygame.draw.rect(surface, self.bgcolor, ttbox.absrect)

            for linenum,line in enumerate(self.text):
                if (self.textalignment == "topLeft"):
                    textpos = ( ttbox.absrect.left , ttbox.absrect.top+linenum*self.font.get_height() )
                elif (self.textalignment == "centre"):
                    textpos = ( (ttbox.absrect.left)/2 , (ttbox.absrect.top+ttbox.absrect.bottom)/2-(self.font.get_height()*len(self.text))/2+(linenum+1)*self.font.get_height()/2 )
                else:
                    textpos = ( ttbox.absrect.left, ttbox.absrect.top+linenum*self.font.get_height() )
                renderTextAtPos(surface,line,textpos,alignment=self.textalignment,font=self.font,color=self.textcolor,backgroundcolor=self.bgcolor)


"""


"""
class Screen:
    def __init__(self,layernames):     
        """Defines the layer structure of the screen. 
        Parameters: 
        layernames is a list of layers from top to bottom"""
        self.NUMLAYERS = len(layernames)

        #layers from top to bottom
        self.layers = []
        for name in layernames:
            newlayer = Layer(name)
            newlayer.surface.fill(ALPHACOLOR)
            newlayer.surface.set_colorkey(ALPHACOLOR)
            self.layers.append(newlayer)
        return

    def clear(self):
        for layer in range(len(self.layers)):
             self.layers[layer].surface.fill(ALPHACOLOR)
    
    def setLayer(self,name,source):
        success = False
        for layer in range(self.NUMLAYERS):
            if (self.layers[layer].name == name):
                success = True
                self.layers[layer].surface.blit(source,(0,0))

        if not success:
            raise Exception("Layer " + name + " does not exist")

    def getLayer(self,name):
        for layer in self.layers:
            if (layer.name == name):
                return layer.surface
        raise Exception("Layer " + name + " does not exist")

    def clearLayer(self,name):
        for layer in self.layers:
            if (layer.name == name):
                layer = Layer(name)
                return
        raise Exception("Layer " + name + " does not exist")

    def draw(self,surface):
        for layer in reversed(self.layers):
            surface.blit(layer.surface,(0,0))
        return

class Layer:
    def __init__(self,name):
        self.name = name
        self.surface = pygame.Surface(screenDims)
        return        

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
        raise Exception("textRenderer: invalid position alignment argument")

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