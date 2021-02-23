"""
here's ur damn docstring
"""

import sys
from random import shuffle
import pygame
from classes import Beast, Equipment, Attack
from scenemanager import Scene, fetchFlags
import eventhandlers
import ui
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode(ui.screenDims)

#Build database and import beasts - move this somewhere else
Attack1 = Attack(name="Slam",power=1.00,element="physical",accuracy=0.90)
Attack2 = Attack(name="Ray of fire",power=0.80,element="heat",accuracy=1.00)
Attack3 = Attack(name="Frosty freezy freeze",power=0.80,element="heat",accuracy=1.00)
Attack4 = Attack(name="Fake out",power=0.80,element="heat",accuracy=1.00)
Attack5 = Attack(name="Taunt",power=0.80,element="heat",accuracy=1.00)
Attack6 = Attack(name="Enrage",power=0.80,element="heat",accuracy=1.00)
Attack7 = Attack(name="Tail swipe",power=0.80,element="heat",accuracy=1.00)
Attack8 = Attack(name="Never gonna give you up",power=0.80,element="heat",accuracy=1.00)
Attack9 = Attack(name="Violent diarrhoea",power=0.80,element="heat",accuracy=1.00)
Attack10 = Attack(name="Lick wounds",power=0.80,element="heat",accuracy=1.00)

Equipment1 = Equipment(name="Metal chestplate",attacks=[Attack1,Attack2,Attack3,Attack4,Attack5,Attack6,Attack7,Attack8,Attack9,Attack10],statbonuses=[("maxHP",+50),("DEF",+20),("shockRES",-0.30)])

Beast1 = Beast("Greg", maxHP = 110, ATK = 100, DEF = 100, heatRES = 0.30, coldRES = -0.20, shockRES = 0, SPE = 100)
Beast1.equipItem(Equipment1)

Beast2 = Beast("Bob", maxHP = 34, ATK = 100, DEF = 100, heatRES = 0.30, coldRES = -0.20, shockRES = 0, SPE = 100)
Beast2.equipItem(Equipment1)

Beast3 = Beast("Micheala", maxHP = 92, ATK = 112, DEF = 100, heatRES = 0, coldRES = 0, shockRES = 0, SPE = 105)
Beast3.equipItem(Equipment1)

Beast4 = Beast("Larissa", maxHP = 186, ATK = 112, DEF = 100, heatRES = 0, coldRES = 0, shockRES = 0, SPE = 105)
Beast4.equipItem(Equipment1)
#end of database

scene = Scene()
scene.addBeast(beast = Beast1,slot = 1)
scene.addBeast(beast = Beast2,slot = 2)
scene.addBeast(beast = Beast3,slot = 3)
scene.addBeast(beast = Beast4,slot = 4)

scene.setupBattle()
ui.drawScene(screen,scene)
pygame.display.flip()

scene.beasts[1].HP = int(round(scene.beasts[1].maxHP*(0.67)))
scene.beasts[2].HP = int(round(scene.beasts[2].maxHP*(0.07)))
scene.beasts[3].HP = int(round(scene.beasts[3].maxHP*(0.43)))
scene.beasts[4].HP = int(round(scene.beasts[4].maxHP*(0.99)))
ui.drawScene(screen,scene)
pygame.display.flip()

battle_active = True
winner = 0
active_flag = None
state = "Idle"
mouseclick = None
flag_name = None
active_beast = None
menuButtons = []
while (battle_active):
    #this is when pygame events get processed so the game doesn't crash
    for event in pygame.event.get():
        #handle inputs, put statemachine here
        if (state == "Choose attack"):
            if (event.type == pygame.MOUSEBUTTONUP):
                if (event.button == 1):
                    for but_id, button in enumerate(menuButtons):
                        if (button.collidemouse()):
                            if (but_id <= len(active_beast.attacks)):
                                active_beast.selectattack(but_id)
                                state = "Choose target"

    #check for raised event flags and sort flags
    raisedFlags = fetchFlags(scene)

    #if no flags are being handled right now, get the next flag
    if (active_flag == None):
        active_flag = raisedFlags.pop(0)
        flag_name = active_flag[0]
        active_beast = scene.beasts[active_flag[1]]
        if (flag_name == "choose_attack"):
            state = "Choose attack"
        elif (flag_name == "execute_attack"):
            state = "Execute attack"
        else:
            state = "Idle"

    #update ui according to state
    if (state == "Idle"):
        menuButtons = []
        ui.drawScene(screen,scene)
        pygame.display.flip()
    elif (state == "Choose attack"):
        ui.drawScene(screen,scene)
        menuButtons = ui.drawMoveselect(screen,active_beast)
        pygame.display.flip()                    
    elif (state == "Choose target"):
        ui.drawScene(screen,scene)
        ui.drawTargetSelect(screen,scene,active_beast)
        pygame.display.flip()
    elif (state == "Execute attack"):
        ui.drawScene(screen,scene)
        pygame.display.flip()
    else:
        pass

    #if flag is resolved, set active flag to None
    #active_flag = None

    #if no events need to be processed, progress game one tick
    if (not raisedFlags):
        scene.tick()
    
    #check if only one teams beasts are remaining (that teams wins, and the battle ends)
    if (not (scene.beasts[1].isalive or scene.beasts[2].isalive)):
        battle_active = False
        winner = "B"
    elif (not (scene.beasts[3].isalive or scene.beasts[4].isalive)):
        battle_active = False
        winner = "A"

    mouseclick = None


scene.printScene()
print("Team " + winner + " wins!")