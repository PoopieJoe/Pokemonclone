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

def renderTextAtPos(surface,text,pos,alignment="topLeft",font=None,color=pygame.Color(255,255,255)):
    if (font==None):
        font = DEFAULTFONT

    textSurface = font.render(text,1,color)
    if (alignment == "topLeft"):
        textpos=pos
    if (alignment == "topCentre"):
        textpos = (pos[0] - textSurface.get_width()/2, pos[1])
    if (alignment == "centreLeft"):
        textpos = (pos[0], pos[1] - textSurface.get_height()/2)
    if (alignment == "centreRight"):
        textpos = (pos[0] - textSurface.get_width(),pos[1] - textSurface.get_height()/2)

    backFill = pygame.surface.Surface((textSurface.get_width(),textSurface.get_height()))
    backFill.fill(BACKGROUNDCOLOR)
    surface.blit(backFill,textpos)
    surface.blit(textSurface,textpos)
    return Rect(textpos,(textSurface.get_width(),textSurface.get_height()))

def drawScene(surface,scene):
    surface.fill(BACKGROUNDCOLOR)
    renderTextAtPos(surface,"Battle title",(surface.get_width()/2,0),"topCentre")

    slotreltextpos = [  
        (0,0),
        (0.05,0.6),
        (0.05,0.7),
        (0.6,0.2),
        (0.6,0.3)
    ]

    for slot, beast in enumerate(scene.beasts[1:],start=1):
        if beast.isalive:
            healthfrac = beast.HP/beast.maxHP
            slottext = beast.name + " " + str(beast.HP) + "/" + str(beast.maxHP) + " HP (" + str(max(round(healthfrac*100),1)) + "%)"
            textpos = multtuple(slotreltextpos[slot],screenDims)

            HPbaroffset = (0,int(NAMEFONTSIZE)/2)
            Hpbarwidth = int(screenDims[0]*(0.33))
            Hpbarheight = int(screenDims[1]*(0.02))
            HPbarposition = addtuple(textpos,HPbaroffset)

            pygame.draw.rect(surface,HPBACKGROUNDCOLOR,(HPbarposition,(Hpbarwidth,Hpbarheight)))
            pygame.draw.rect(surface,HPFOREGROUNDCOLOR,(HPbarposition,(Hpbarwidth*healthfrac,Hpbarheight)))
            renderTextAtPos(surface,slottext,textpos,"centreLeft",font=NAMEFONT)
    return

def addtuple(xs,ys):
     return tuple(x + y for x, y in zip(xs, ys))
    
def multtuple(xs,ys):
    return tuple(x * y for x, y in zip(xs, ys))