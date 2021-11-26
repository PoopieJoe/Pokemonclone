import pygame
from pygame.locals import *
pygame.init()
#### Gameplay-related constants

BEASTSPERTEAM = 2

# Elements
ELEMENTS = ["physical","heat","cold","shock"]

# Under the hood constants
TURNTRACKER_LENGTH = 20000 #time unit for 1 full turn (between move selections). Since monsters move their speed every tick, at average speed of 100, it takes 100 ticks from move selection to attack, and 100 ticks from attack back to move selection

# Randomness
attackroll_randmod = 0.1 #attacks deal randomly between 90% and 110% dmg
critchance = 0.05 #5% critchance
critmulti = 1.5 #critical hit dmg multiplier

# Flags
MULTIHITNAME = "Multihit"
TARGETOTHERSTR = "Target_other"
TARGETTEAMSTR = "Target_team"
TARGETTEAMSTR = "Target_all_others"

# Status effects
BURNNAME = "Burn"
BURNDMG = 1/8 #dmg per 100 ticks
BURNTOOLTIP = "Take continuous damage over time"

SLOWNAME = "Slow"
SLOWMOD = 0.5 #speed multiplier during slow
SLOWTOOLTIP = "Reduced speed"

# UI colors and fonts
screenDims = (1280,720)

ALPHACOLOR = pygame.Color(0,1,255)
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

# Colors to differentiate between slots
SLOT1COLOR = Color(255,0,0)
SLOT2COLOR = Color(0,255,0)
SLOT3COLOR = Color(0,0,255)
SLOT4COLOR = Color(255,180,0)