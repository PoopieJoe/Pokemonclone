import pygame
from pygame.locals import *
import scenemanager
import classes
from math import floor

pygame.init()

screenDims = (1280,720)

DEFAULTFONT = pygame.font.SysFont(None,int(screenDims[1]/(360/50)))
NAMEFONT = pygame.font.SysFont(None,int(screenDims[1]/(360/20)))
BACKGROUNDCOLOR = pygame.Color(80,158,40)
BACKGROUND = pygame.surface.Surface(screenDims).fill(BACKGROUNDCOLOR)

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
    slot1Text = scene.beasts[1].name + " " + str(scene.beasts[1].HP) + "/" + str(scene.beasts[1].maxHP) + " HP (" + str(floor(scene.beasts[1].HP/scene.beasts[1].maxHP*100)) + "%)"
    slot3Text = scene.beasts[3].name + " " + str(scene.beasts[3].HP) + "/" + str(scene.beasts[3].maxHP) + " HP (" + str(floor(scene.beasts[3].HP/scene.beasts[3].maxHP*100)) + "%)"
    
    renderTextAtPos(screen,"Battle title",(screen.get_width()/2,0),"topCentre")
    renderTextAtPos(surface,slot1Text,(0,int(screenDims[1]*(0.6))),"centreLeft",font=NAMEFONT)
    renderTextAtPos(surface,slot3Text,(screenDims[0]*(0.6),int(screenDims[1]*(0.2))),"centreLeft",font=NAMEFONT)
    return