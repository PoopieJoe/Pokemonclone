"""
here's ur damn docstring
"""

import sys
from random import shuffle
import pygame
from time import sleep
from classes import *
from scenemanager import Scene, fetchFlags
import eventhandlers
import ui
#from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode(ui.screenDims)

#Build a beast
Beast1 = Beast(getSpecies("Lurker"),nickname="Greg",loadout=[None,getEquipment("Metal chestplate"),None,None,None])
Beast1.maxHP = 10000
Beast1.HP = Beast1.maxHP
Beast2 = Beast(getSpecies("Viper"),nickname="Bob",loadout=[None,getEquipment("Metal chestplate"),getEquipment("Tail blade")])
Beast3 = Beast(getSpecies("Lizion"),nickname="Micheala",loadout=[getEquipment("Icy mask"),None,None,None,getEquipment("Tail blade")])
Beast4 = Beast(getSpecies("Halfling"),nickname="Claire",loadout=[None,getEquipment("Metal chestplate"),None,None,None])

scene = Scene()
scene.addBeast(beast = Beast1,slot = 1)
scene.addBeast(beast = Beast2,slot = 2)
scene.addBeast(beast = Beast3,slot = 3)
scene.addBeast(beast = Beast4,slot = 4)

scene.setupBattle()
ui.drawScene(screen,scene)
pygame.display.flip()

raisedFlags = []
battle_active = True
winner = 0
active_flag = None
state = "Idle"
flag_name = None
active_beast = None
menuButtons = []
attackresult = []
while (battle_active):
    #this is when pygame events get processed so the game doesn't crash
    for event in pygame.event.get():
        #handle inputs, put statemachine here
        if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
            if (state == "Choose attack"):
                for but_id, button in enumerate(menuButtons):
                    if (button.collidemouse()):
                        if (button.id >= 0 and button.id <= 12):
                            active_beast.selectattack(button.id)
                            state = "Choose target"
            elif (state == "Choose target"):
                for but_id, button in enumerate(menuButtons):
                    if (button.collidemouse()):
                        if (button.id >= 1 and button.id <= 4):
                            active_beast.selecttarget(scene,button.id)
                            active_beast.clearflag(1)
                            state = "Idle"
                            active_flag = None
            elif (state == "Execute attack"):
                for but_id, button in enumerate(menuButtons):
                    if (button.collidemouse()):
                        if (button.type == "continue"):
                            state = "Idle"
                            active_flag = None



    #check for raised event flags and sort flags
    if ((active_flag == None) and (len(raisedFlags) == 0)):
        raisedFlags = fetchFlags(scene)

    #if no flags are being handled right now, get the next flag
    if ((active_flag == None) and (len(raisedFlags) > 0)):
        active_flag = raisedFlags.pop(0)
        flag_name = active_flag[0]
        active_beast = scene.beasts[active_flag[1]]
        if (flag_name == "choose_attack"):
            state = "Choose attack"
        elif (flag_name == "execute_attack"):
            attackresult = []
            state = "Execute attack"
        else:
            state = "Idle"

    #change gamestate according to state
    if (state == "Execute attack"):
        if (active_beast.getflag(0)):
            #TODO: multitarget attacks handled here?
            attackresult.append( eventhandlers.performattack(active_beast,scene.beasts[active_beast.selected_attack[1]]) )
            if (attackresult[0]["chain"]["type"] == "num_left"):
                #chains multiple identical attack
                chainsleft = attackresult[0]["chain"]["value"]
                while (chainsleft > 0):
                    attackresult.append( eventhandlers.performattack(active_beast,scene.beasts[active_beast.selected_attack[1]],chained = True) )
                    chainsleft = chainsleft - 1
            elif (attackresult[0]["chain"]["type"] == "by_id"):
                print("yea no this doesnt work yet")
                pass
            active_beast.clearflag(0)
            active_beast.selected_attack = [None,0]

    #update ui according to state
    if (state == "Idle"):
        menuButtons = []
        ui.drawScene(screen,scene)
        pygame.display.flip()
    elif (state == "Choose attack"):
        ui.drawScene(screen,scene)
        menuButtons = ui.drawMoveselect(screen,scene,active_beast)
        pygame.display.flip()
    elif (state == "Choose target"):
        ui.drawScene(screen,scene)
        menuButtons = ui.drawTargetSelect(screen,scene,active_beast)
        pygame.display.flip()
    elif (state == "Execute attack"):
        if (attackresult):
            ui.drawScene(screen,scene)
            menuButtons = ui.drawExecuteAttack(screen,scene,attackresult)
            pygame.display.flip()
    else:
        pass

    #if no events need to be processed, progress game one tick
    if (len(raisedFlags) == 0 and state == "Idle"):
        sleep(1/30) #worlds shittiestly programmed framerate
        scene.tick()
    
    #check if only one teams beasts are remaining (that teams wins, and the battle ends)
    if (not (scene.beasts[1].isalive or scene.beasts[2].isalive)):
        battle_active = False
        winner = "B"
    elif (not (scene.beasts[3].isalive or scene.beasts[4].isalive)):
        battle_active = False
        winner = "A"

scene.printScene()
print("Team " + winner + " wins!")