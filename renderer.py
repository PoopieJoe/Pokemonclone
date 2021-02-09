import pygame
from pygame.locals import *
import scenemanager
import classes
from math import floor

pygame.init()

screenDims = (1280,720)

defFont = pygame.font.SysFont(None,int(screenDims[1]/(360/50)))
nameFont = pygame.font.SysFont(None,int(screenDims[1]/(360/20)))
backgroundColor = pygame.Color(80,158,40)
background = pygame.surface.Surface(screenDims).fill(backgroundColor)

def renderTextAtPos(surface,text,pos,alignment="topLeft",font=None,color=pygame.Color(255,255,255)):
    if (font==None):
        font = defFont

    textSurface = font.render(text,1,color)
    if (alignment == "topLeft"):
        textpos=pos
    if (alignment == "topCentre"):
        textpos = (pos[0] - textSurface.get_width()/2, pos[1])
    if (alignment == "centreLeft"):
        textpos = (pos[0], pos[1] - textSurface.get_height()/2)
    if (alignment == "centreRight"):
        textpos = (pos[0] - textSurface.get_width(),pos[1] - textSurface.get_height()/2)

    surface.blit(textSurface,textpos)
    return

def drawScene(surface,scene):
    slot1Text = scene.beasts[1].name.ljust(16," ") + str(scene.beasts[1].HP).ljust(3," ") + "/" + str(scene.beasts[1].maxHP).ljust(3," ") + " HP (" + str(floor(scene.beasts[1].HP/scene.beasts[1].maxHP*100)).ljust(3," ") + "%)"
    slot3Text = scene.beasts[3].name.ljust(16," ") + str(scene.beasts[3].HP).ljust(3," ") + "/" + str(scene.beasts[3].maxHP).ljust(3," ") + " HP (" + str(floor(scene.beasts[3].HP/scene.beasts[3].maxHP*100)).ljust(3," ") + "%)"
    
    renderTextAtPos(surface,slot1Text,(0,int(screenDims[1]*(0.6))),"centreLeft",font=nameFont)
    renderTextAtPos(surface,slot3Text,(screenDims[0],int(screenDims[1]*(0.2))),"centreRight",font=nameFont)
    return