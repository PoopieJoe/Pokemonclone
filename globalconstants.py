import pygame
from pygame.locals import *
pygame.init()
#### Gameplay-related constants

BEASTSPERTEAM = 2

# Elements
PHYSNAME = "Physical"
HEATNAME = "Heat"
COLDNAME = "Cold"
SHOCKNAME = "Shock"
ELEMENTS = [PHYSNAME,HEATNAME,COLDNAME,SHOCKNAME]

# Under the hood constants
TURNTRACKER_LENGTH = 20000 #time unit for 1 full turn (between move selections). Since monsters move their speed every tick, at average speed of 100, it takes 100 ticks from move selection to attack, and 100 ticks from attack back to move selection

# Randomness
attackroll_randmod = 0.1 #attacks deal randomly between 90% and 110% dmg
critchance = 0.05 #5% critchance
critmulti = 1.5 #critical hit dmg multiplier

# Chain
NOCHAINID = -1

# Flags
MULTIHITNAME = "Multihit"
TARGETOTHER = "Target_other"
TARGETTEAM = "Target_team"
TARGETALLOTHER = "Target_all_others"
TARGETSELF = "Target_self"
TARGETANY = "Target_any"
TARGETNONE = "Target_none"
CONTACTFLAG = "Contact"

# Equipment effects
REFLECTNAME = "Reflect"
REFLECTBASEVAL = 0.1 #reflects 10% of dmg taken per level

# Status effects

VALUENONE = -1 #default values for secondary effect value and chance
CHANCENONE = -1

MULTIHITNAME = "Multihit"

BURNNAME = "Burn"
BURNDMG = 1/8 #dmg per 100 ticks
BURNTOOLTIP = "Take continuous damage over time"

SLOWNAME = "Slow"
SLOWMOD = 0.5 #speed multiplier during slow
SLOWBASEDURATION = 1/6 #slows for 1/6th of a turn per level
SLOWTOOLTIP = "Reduced speed"

# State flags
FLAG_CHOOSEATTACK = "FLAG_CHOOSEATTACK"
FLAG_EXECUTEATTACK = "FLAG_EXECUTEATTACK"

# Game states
STATE_START = "Start"
STATE_MAINMENU = "Main menu"
STATE_VIEWTEAMS = "View teams"
STATE_EDITTEAM = "Edit team"
STATE_CHOOSEATTACK = "Choose attack"
STATE_CHOOSETARGET = "Choose target"
STATE_EXECUTEATTACK = "Execute attack"
STATE_IDLE = "Idle"

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