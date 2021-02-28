"""
here's ur damn docstring
"""

import sys
from random import shuffle
import pygame
from classes import *
from scenemanager import Scene, fetchFlags
import eventhandlers
import ui
#from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode(ui.screenDims)


#Build database and import beasts - move this somewhere else
Beast1 = Beast(getSpecies("Lurker"),nickname="Greg",loadout=[None,getEquipment("Metal chestplate"),None,None,None])
Beast2 = Beast(getSpecies("Lurker"),nickname="Bob",loadout=[None,getEquipment("Metal chestplate"),None,None,None])
Beast3 = Beast(getSpecies("Viper"),nickname="Micheala",loadout=[None,getEquipment("Metal chestplate"),None])
Beast4 = Beast(getSpecies("Viper"),nickname="Claire",loadout=[None,getEquipment("Metal chestplate"),None])

scene = Scene()
scene.addBeast(beast = Beast1,slot = 1)
scene.addBeast(beast = Beast2,slot = 2)
scene.addBeast(beast = Beast3,slot = 3)
scene.addBeast(beast = Beast4,slot = 4)

scene.setupBattle()
ui.drawScene(screen,scene)
pygame.display.flip()

#scene.beasts[1].HP = int(round(scene.beasts[1].maxHP*(0.67)))
#scene.beasts[2].HP = int(round(scene.beasts[2].maxHP*(0.07)))
#scene.beasts[3].HP = int(round(scene.beasts[3].maxHP*(0.43)))
#scene.beasts[4].HP = int(round(scene.beasts[4].maxHP*(0.99)))
#for beast in scene.beasts[1:]:
#    beast.addstatuseffect("Poison")
#ui.drawScene(screen,scene)
#pygame.display.flip()

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
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                for but_id, button in enumerate(menuButtons):
                    if (button.collidemouse()):
                        if (button.id >= 0 and button.id <= 12):
                            active_beast.selectattack(button.id)
                            state = "Choose target"
        elif (state == "Choose target"):
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                for but_id, button in enumerate(menuButtons):
                    if (button.collidemouse()):
                        if (button.id >= 1 and button.id <= 4):
                            active_beast.selecttarget(scene,button.id)
                            active_beast.clearflag(1)
                            state = "Idle"
                            active_flag = None

    #check for raised event flags and sort flags
    raisedFlags = fetchFlags(scene)

    #if no flags are being handled right now, get the next flag
    if ((active_flag == None) and (len(raisedFlags) > 0)):
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
        menuButtons = ui.drawTargetSelect(screen,scene,active_beast)
        pygame.display.flip()
    elif (state == "Execute attack"):
        ui.drawScene(screen,scene)
        eventhandlers.performattack(scene,active_beast)
        active_beast.clearflag(0)
        state = "Idle"
        active_flag = None
        pygame.display.flip()
    else:
        pass

    #if flag is resolved, set active flag to None
    #active_flag = None

    #if no events need to be processed, progress game one tick
    if (len(raisedFlags) == 0):
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