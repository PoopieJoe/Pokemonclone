"""
here's ur damn docstring
"""

import sys
from random import shuffle
import pygame
from classes import Beast, Equipment, Attack
from scenemanager import Scene
import eventhandlers
import renderer
#from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode(renderer.screenDims)

#Build database and import beasts - move this somewhere else
Attack1 = Attack(name="Slam",power=1.00,element="physical",accuracy=0.90)
Attack2 = Attack(name="Ray of Fire",power=0.80,element="heat",accuracy=1.00)

Equipment1 = Equipment(name="Metal chestplate",attacks=[Attack1,Attack2],statbonuses=[("maxHP",+50),("DEF",+20),("shockRES",-0.30)])

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
renderer.drawScene(screen,scene)
pygame.display.flip()

scene.beasts[1].HP = int(round(scene.beasts[1].maxHP*(0.67)))
scene.beasts[2].HP = int(round(scene.beasts[2].maxHP*(0.07)))
scene.beasts[3].HP = int(round(scene.beasts[3].maxHP*(0.43)))
scene.beasts[4].HP = int(round(scene.beasts[4].maxHP*(0.99)))
renderer.drawScene(screen,scene)
pygame.display.flip()

battle_active = True
winner = 0
while (battle_active):
    #check for raised event flags and sort flags
    #rules: from first resolved to last resolved: choose move, attacks
    #       multiple flags of the same type are resolved in random order
    choose_attack_list = []
    execute_attack_list = []
    flaglist = [choose_attack_list,execute_attack_list]
    for slot, beast in enumerate(scene.beasts[1:],start=1):
        for flag in beast.flags:
            if (flag[1]):
                if (flag[0] == "choose_attack"):
                    choose_attack_list.append(slot)
                elif (flag[0] == "execute_attack"):
                    execute_attack_list.append(slot)

    #Shuffle flags with same priority
    for sublist in flaglist:
        shuffle(sublist)

    #resolve events
    for flag_id, sublist in enumerate(flaglist,start=0):
        if (flag_id == 0):
            for slot in sublist:
                eventhandlers.moveselect(scene,slot,screen)
        if (flag_id == 1):
            for slot in sublist:
                eventhandlers.performattack(scene,slot)

    #progress game one tick
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