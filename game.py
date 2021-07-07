"""
here's ur damn docstring
"""

import sys
from random import shuffle
import pygame
from classes import *
from scenemanager import Scene
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

battle_active = True
winner = 0
menuButtons = []
while (battle_active):
    #this is when pygame events get processed so the game doesn't crash
    for event in pygame.event.get():
        #handle inputs, put statemachine here
        if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
            for button in menuButtons:
                if button.collidemouse():
                    success = button.action(*(button.actionargs))
                    if success:
                        if scene.state == "Choose attack":
                            scene.state = "Choose target"
                        elif scene.state == "Choose target":
                            scene.active_beast.clearflag(1)
                            scene.state = "Idle"
                            scene.active_flag = None
                        elif scene.state == "Execute attack":
                            scene.attackresult = []
                            scene.active_beast.clearflag(0)
                            scene.state = "Idle"
                            scene.active_flag = None

    #check for raised event flags and sort flags
    if (scene.noflags()):
        scene.fetchFlags()
    scene.popflag()

    #change gamestate according to state
    if (scene.state == "Execute attack"):
        if (scene.active_beast.getflag(0)):
            #TODO: multitarget attacks handled here?
            scene.attackresult.append( eventhandlers.performattack(scene.active_beast,scene.beasts[scene.active_beast.selected_attack[1]]) )
            if (scene.attackresult[0]["chain"]["type"] == "num_left"):
                #chains multiple identical attack
                scene.chainsleft = scene.attackresult[0]["chain"]["value"]
                while (scene.chainsleft > 0):
                    scene.attackresult.append( eventhandlers.performattack(scene.active_beast,scene.beasts[scene.active_beast.selected_attack[1]],chained = True) )
                    scene.chainsleft = scene.chainsleft - 1
            elif (scene.attackresult[0]["chain"]["type"] == "by_id"):
                print("yea no this doesnt work yet")
                pass
            scene.active_beast.clearflag(0)
            scene.active_beast.selected_attack = [None,0]

    scene.tick()

    #update ui according to state
    if (scene.state == "Idle"):
        menuButtons = []
        ui.drawScene(screen,scene)
    elif (scene.state == "Choose attack"):
        ui.drawScene(screen,scene)
        menuButtons = ui.drawMoveselect(screen,scene,scene.active_beast)
    elif (scene.state == "Choose target"):
        ui.drawScene(screen,scene)
        menuButtons = ui.drawTargetSelect(screen,scene,scene.active_beast)
    elif (scene.state == "Execute attack"):
        if (scene.attackresult):
            ui.drawScene(screen,scene)
            menuButtons = ui.drawExecuteAttack(screen,scene,scene.attackresult)
    else:
        pass

    pygame.display.flip()
    
    #check if only one teams beasts are remaining (that teams wins, and the battle ends)
    if (not (scene.beasts[1].isalive or scene.beasts[2].isalive)):
        battle_active = False
        winner = team2name
    elif (not (scene.beasts[3].isalive or scene.beasts[4].isalive)):
        battle_active = False
        winner = team1name

scene.printScene()
print("Team " + winner + " wins!")