"""
here's ur damn docstring
"""

import sys
from time import sleep
from pathlib import Path
import pygame
import thorpy
import core
from scenemanager import Scene
import classes as c
import ui
from globalconstants import *
import teamimport as timport

#from pygame.locals import *

pygame.init()

# SETUP

application = thorpy.Application((SCREENW,SCREENH), "Pokemonclone")

game = core.CoreGame()

game.launch()

application.quit()
pygame.quit()

##############################################################################
# #Import teams from file:
# Team1 = timport.importteam(Path("./teams/Test_3.txt"))
# Team2 = timport.importteam(Path("./teams/Test_2.txt"))
# teams = [Team1,Team2]

# #Build scene
# scene = Scene()
# for teamn,team in enumerate(teams):
#     for beast in team.beasts:
#         scene.addBeast(beast,team = teamn)

# scene.setupBattle()

# #initialize ui
# windowoutput = pygame.display.set_mode(ui.screenDims)
# screen = ui.Screen([    "tooltips",
#                         "overlay",
#                         "background"])

# ui.drawScene(screen,scene)
# windowoutput.fill(BACKGROUNDCOLOR)
# screen.draw(windowoutput)
# pygame.display.flip()

# battle_active = True
# menuButtons = []
# while (battle_active):
#     for event in pygame.event.get():
#         #handle inputs, put statemachine here
#         if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1): #left mousebutton up
#             for button in menuButtons:
#                 if button.collidemouse():
#                     success = button.action(*(button.actionargs))
#                     if success:
#                         if scene.state == STATE_CHOOSEATTACK:
#                             scene.state = STATE_CHOOSETARGET
#                         elif scene.state == STATE_CHOOSETARGET:
#                             scene.active_slot.beast.clearflag(FLAG_CHOOSEATTACK)
#                             scene.state = STATE_IDLE
#                             scene.active_flag = None
#                         elif scene.state == STATE_EXECUTEATTACK:
#                             scene.attackresult = []
#                             scene.active_slot.beast.clearflag(FLAG_EXECUTEATTACK)
#                             scene.state = STATE_IDLE
#                             scene.active_flag = None
#         else:
#             pass

#     #check for raised event flags and sort flags
#     if (scene.noflags()):
#         scene.fetchFlags()
#     scene.popflag()

#     #change gamestate according to state
#     if (scene.state == STATE_EXECUTEATTACK):
#         if (scene.active_slot.beast.selected_attack.atk != None):
#             scene.processattack()
#     elif (len(scene.raisedFlags) == 0 and scene.state == STATE_IDLE):
#         scene.tick()

#     sleep(1/60) #worlds shittiestly programmed framerate

#     #wipe internal buffer
#     screen.clear()
#     #update ui according to state
#     if (scene.state == STATE_IDLE):
#         menuButtons = []
#         ui.drawScene(screen,scene)
#     elif (scene.state == STATE_CHOOSEATTACK):
#         menuButtons = ui.drawMoveselect(screen,scene,scene.active_slot)
#     elif (scene.state == STATE_CHOOSETARGET):
#         ui.drawScene(screen,scene)
#         menuButtons = ui.drawTargetSelect(screen,scene,scene.active_slot)
#     elif (scene.state == STATE_EXECUTEATTACK):
#         if (scene.attackresult):
#             ui.drawScene(screen,scene)
#             menuButtons = ui.drawExecuteAttack(screen,scene,scene.attackresult)
#     else:
#         pass #just black screen?

#     screen.draw(windowoutput)
#     pygame.display.flip()
    
#     #check if only one teams beasts are remaining (that teams wins, and the battle ends)
#     if (not (scene.slots[0].beast.isalive or scene.slots[1].beast.isalive)):
#         battle_active = False
#         winner = Team2.name
#     elif (not (scene.slots[2].beast.isalive or scene.slots[3].beast.isalive)):
#         battle_active = False
#         winner = Team1.name

# scene.printScene()
# print("Team " + winner + " wins!")