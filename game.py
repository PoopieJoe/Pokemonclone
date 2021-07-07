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
Beast1 = Beast(species="Lurker",nickname="Greg",loadout=[None,"Metal chestplate",None,None,None])
Beast2 = Beast(species="Viper",nickname="Bob",loadout=[None,"Metal chestplate","Tail blade"])

Beast3 = Beast(species="Lizion",nickname="Micheala",loadout=["Icy mask",None,None,None,"Tail blade"])
Beast4 = Beast(species="Halfling",nickname="Claire",loadout=[None,"Metal chestplate",None,None,None])

team1name = Beast1.nickname + " & " + Beast2.nickname
team2name = Beast3.nickname + " & " + Beast4.nickname

#Build scene
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
            #TODO: handle button presses better
            for button in menuButtons:
                if button.collidemouse():
                    success = button.action(*(button.actionargs))
                    if success:
                        if state == "Choose attack":
                            state = "Choose target"
                        elif state == "Choose target":
                            active_beast.clearflag(1)
                            state = "Idle"
                            active_flag = None
                        elif state == "Execute attack":
                            active_beast.clearflag(0)
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
        winner = team2name
    elif (not (scene.beasts[3].isalive or scene.beasts[4].isalive)):
        battle_active = False
        winner = team1name

scene.printScene()
print("Team " + winner + " wins!")