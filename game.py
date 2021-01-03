from classes import *
from printdetails import printFullBeastStatus
from scenemanager import Scene
from random import shuffle
import eventhandlers
import pygame
#from pygame.locals import *

pygame.init()

Attack1 = Attack(name="Slam",power=1.00,element="physical",accuracy=0.90)
Attack2 = Attack(name="Ray of Fire",power=0.80,element="heat",accuracy=1.00)

Equipment1 = Equipment(name="Metal chestplate",attacks=[Attack1,Attack2],statbonuses=[("maxHP",+50),("DEF",+20),("shockRES",-0.30)])

Beast1 = Beast("Greg", maxHP = 110, ATK = 100, DEF = 100, heatRES = 0.30, coldRES = -0.20, shockRES = 0, SPE = 100)
Beast1.equipItem(Equipment1)

Beast2 = Beast("Micheala", maxHP = 92, ATK = 112, DEF = 100, heatRES = 0, coldRES = 0, shockRES = 0, SPE = 105)
Beast2.equipItem(Equipment1)

scene = Scene()
scene.addBeast(beast = Beast1,slot = 1)
scene.addBeast(beast = Beast2,slot = 3)

scene.setupBattle()
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
        resolve_function = [eventhandlers.moveselect,eventhandlers.performattack][flag_id]
        for slot in sublist:
            resolve_function(scene,slot)
    
    #check if only one teams beasts are remaining (that teams wins, and the battle ends)
    if (not (scene.beasts[1].isalive or scene.beasts[2].isalive)):
        battle_active = False
        winner = "B"
    elif (not (scene.beasts[3].isalive or scene.beasts[4].isalive)):
        battle_active = False
        winner = "A"

    #progress game one tick
    scene.tick()

scene.printScene()
print("Team " + winner + " wins!")