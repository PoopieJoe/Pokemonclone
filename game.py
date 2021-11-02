"""
here's ur damn docstring
"""

import sys
from pathlib import Path
from random import shuffle
import pygame
import classes as c
from scenemanager import Scene
import eventhandlers as evth
import ui
import globalconstants as gconst
import teamimport as timport
#from pygame.locals import *

pygame.init()

#Import teams from file:
Team1 = timport.importteam(Path("./teams/Test_1.txt"))
Team2 = timport.importteam(Path("./teams/Test_2.txt"))

#Build scene
scene = Scene()
scene.addBeast(beast = Team1.beasts[0],slot = 1)
scene.addBeast(beast = Team1.beasts[1],slot = 2)
scene.addBeast(beast = Team2.beasts[0],slot = 3)
scene.addBeast(beast = Team2.beasts[1],slot = 4)

scene.setupBattle()

#initialize ui
windowoutput = pygame.display.set_mode(ui.screenDims)
screen = ui.Screen([    "tooltips",
                        "overlay",
                        "background"])
ui.drawScene(screen,scene)
windowoutput.fill(gconst.BACKGROUNDCOLOR)
screen.draw(windowoutput)
pygame.display.flip()

battle_active = True
menuButtons = []
while (battle_active):
    for event in pygame.event.get():
        #handle inputs, put statemachine here
        if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1): #left mousebutton up
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
        else:
            pass

    #check for raised event flags and sort flags
    if (scene.noflags()):
        scene.fetchFlags()
    scene.popflag()

    #change gamestate according to state
    if (scene.state == "Execute attack"):
        if (scene.active_beast.getflag(0)):
            #TODO: multitarget attacks handled here?
            scene.attackresult.append( evth.performattack(scene.active_beast,scene.beasts[scene.active_beast.selected_attack[1]]) )
            if (scene.attackresult[0]["chain"]["type"] == "num_left"):
                #chains multiple identical attack
                scene.chainsleft = scene.attackresult[0]["chain"]["value"]
                while (scene.chainsleft > 0):
                    scene.attackresult.append( evth.performattack(scene.active_beast,scene.beasts[scene.active_beast.selected_attack[1]],chained = True) )
                    scene.chainsleft = scene.chainsleft - 1
            elif (scene.attackresult[0]["chain"]["type"] == "by_id"):
                print("yea no this doesnt work yet")
                pass
            scene.active_beast.clearflag(0)
            scene.active_beast.selected_attack = [None,0]

    if (len(scene.raisedFlags) == 0 and scene.state == "Idle"):
        scene.tick()

    #wipe internal buffer
    screen.clear()
    #update ui according to state
    if (scene.state == "Idle"):
        menuButtons = []
        ui.drawScene(screen,scene)
    elif (scene.state == "Choose attack"):
        menuButtons = ui.drawMoveselect(screen,scene,scene.active_beast)
    elif (scene.state == "Choose target"):
        ui.drawScene(screen,scene)
        menuButtons = ui.drawTargetSelect(screen,scene,scene.active_beast)
    elif (scene.state == "Execute attack"):
        if (scene.attackresult):
            ui.drawScene(screen,scene)
            menuButtons = ui.drawExecuteAttack(screen,scene,scene.attackresult)
    else:
        pass #just black screen?

    screen.draw(windowoutput)
    pygame.display.flip()
    
    #check if only one teams beasts are remaining (that teams wins, and the battle ends)
    if (not (scene.beasts[1].isalive or scene.beasts[2].isalive)):
        battle_active = False
        winner = Team2.name
    elif (not (scene.beasts[3].isalive or scene.beasts[4].isalive)):
        battle_active = False
        winner = Team1.name

scene.printScene()
print("Team " + winner + " wins!")