import pygame
from pygame.locals import *
pygame.init()
#### Gameplay-related constants

# Elements
ELEMENTS = ["physical","heat","cold","shock"]

# Under the hood constants
TURNTRACKER_LENGTH = 20000 #time unit for 1 full turn (between move selections). Since monsters move their speed every tick, at average speed of 100, it takes 100 ticks from move selection to attack, and 100 ticks from attack back to move selection

# Randomness
attackroll_randmod = 0.1 #attacks deal randomly between 90% and 110% dmg
critchance = 0.05 #5% critchance
critmulti = 1.5 #critical hit dmg multiplier

# Status effects
BURNNAME = "Burn"
BURNDMG = 1/8 #dmg per turn

SLOWNAME = "Slow"
SLOWMOD = 0.8 #speed multiplier during slow

# UI constants
screenDims = (1280,720)

DEFAULTFONTSIZE = int(screenDims[1]/7.2)
DEFAULTFONT = pygame.font.SysFont(None,DEFAULTFONTSIZE)
NAMEFONTSIZE = int(screenDims[1]*1/25)
NAMEFONT = pygame.font.SysFont(None,NAMEFONTSIZE)

BACKGROUNDCOLOR = pygame.Color(80,158,40)
BACKGROUND = pygame.surface.Surface(screenDims).fill(BACKGROUNDCOLOR)
HPBACKGROUNDCOLOR = pygame.Color(180,180,180)
HPFOREGROUNDCOLOR = pygame.Color(180,0,0)
MOVESELECTBACKGROUNDCOLOR = pygame.Color(200,200,200)
MOVESELECTFOREGROUNDCOLOR = pygame.Color(240,240,240)
MOVESELECTGREY = pygame.Color(150,150,150)
BUTTONHOVERCOLOR = pygame.Color(200,200,255)
BUTTONPRESSCOLOR = pygame.Color(160,160,225)
TRACKERBARCOLOR = pygame.Color(255,255,80)
TESTCOLOR = pygame.Color(255,0,255)

column_buttonlimit = 6
interbox_margin_y = 0.04
interbox_margin_x = 0.01
buttonheight = (1-interbox_margin_y*(column_buttonlimit-1))/column_buttonlimit
buttonfont = pygame.font.SysFont(None,int(200*buttonheight))
statusfont = pygame.font.SysFont(None,int(250*buttonheight))

# Colors to differentiate between slots
SLOT1COLOR = Color(255,0,0)
SLOT2COLOR = Color(0,255,0)
SLOT3COLOR = Color(0,0,255)
SLOT4COLOR = Color(255,255,0)