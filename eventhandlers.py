from math import floor,ceil
from classes import Beast, Attack
from random import random
import pygame
import ui

ELEMENTS = ["physical","heat","cold","shock"]
attackroll_randmod = 0.1 #attacks deal randomly between 90% and 110% dmg
critchance = 0.05 #5% critchance
critmulti = 1.5 #critical hit dmg multiplier

def moveselect(scene,slot,surface):
    scene.printScene()
    beast = scene.beasts[slot]

    ui.drawScene(surface,scene)
    ui.drawMoveselect(surface,beast)
    pygame.display.flip()

    selected_move = None
    selected_slot = 0
    move_selected = False
    while(not move_selected):
        pass


    print("> " + beast.name + " (Slot " + str(slot) + ") will use " + selected_move.name + " on " + scene.beasts[selected_slot].name + " (Slot " + str(selected_slot) + ")!")
    beast.selected_attack = [selected_move,selected_slot]
    scene.turnTracker[slot] = 0
    beast.clearflag(1)
    return

""" #show status
    print("\n> " + beast.name.ljust(16," ") + str(beast.HP).ljust(3," ") + "/" + str(beast.maxHP).ljust(3," ") + " HP (" + str(floor(beast.HP/beast.maxHP*100)).ljust(3," ") + "%)")

    #move select
    movelist = []
    for attack in beast.attacks:
        movelist.append(attack.name)
    print("> Moves: ", end="")
    print(*movelist, sep=", ")

    move_name = input("Select move: ").strip()
    while (move_name not in [attack.name for attack in beast.attacks]):
        print(move_name + " is an invalid move, choose one of the available moves")
        print("> Moves: ", end="")
        print(*movelist, sep=", ")
        move_name = str(input("Select move: ")).strip()
    selected_move = beast.attacks[[attack.name for attack in beast.attacks].index(move_name)]

    #select target  
    print("> Team A: ", end = "")
    print("Slot 1: " + scene.beasts[1].name.ljust(16," ") + ", Slot 2: " + scene.beasts[2].name.ljust(16," "))
    print("> Team B: ", end = "")
    print("Slot 3: " + scene.beasts[3].name.ljust(16," ") + ", Slot 4: " + scene.beasts[4].name.ljust(16," "))

    selected_slot = int(input("Select target slot: ").strip())
    while (selected_slot < 1 or selected_slot > 4 or scene.beasts[selected_slot].name == Beast().name):
        if (selected_slot < 1 or selected_slot > 4):
            print(str(selected_slot) + " is an invalid slot, choose a number between 1 and 4")
        elif (scene.beasts[selected_slot].name == Beast().name):
            print(str(selected_slot) + " is an empty slot, choose a slot with a beast")
        print("> Team A: ", end = "")
        print("Slot 1: " + scene.beasts[1].name.ljust(16," ") + ", Slot 2: " + scene.beasts[2].name.ljust(16," "))
        print("> Team B: ", end = "")
        print("Slot 3: " + scene.beasts[3].name.ljust(16," ") + ", Slot 4: " + scene.beasts[4].name.ljust(16," "))
        selected_slot = int(input("Select target slot: ").strip()) """

def performattack(scene,attackingBeast):
    defendingBeast = scene.beasts[attackingBeast.selected_attack[1]]
    attack = attackingBeast.selected_attack[0]
    attackingBeast.selected_attack = [None,0]

    if (defendingBeast == None):
        print("\n> No target, the attack failed!")
        return
    else:
        print("\n> " + attackingBeast.nickname + " used " + attack.name + " on " + defendingBeast.nickname + "!")

    #determine hit
    if ( random() >= (attack.accuracy) ):
        print("> The attack missed!")
        return

    #if hit, calculate dmg

    #get unmodified damage
    raw_physdmg = attack.power[0]*attackingBeast.physATK
    raw_magdmg = [attackingBeast.magATK*element for element in attack.power[1:]]
    raw_dmg = [raw_physdmg,raw_magdmg[0],raw_magdmg[1],raw_magdmg[2]]

    #get modifiers
    elementalmodifiers = [
        {"added": [], "added total": 0, "multi": [], "multi total" : 1},
        {"added": [], "added total": 0, "multi": [], "multi total" : 1},
        {"added": [], "added total": 0, "multi": [], "multi total" : 1},
        {"added": [], "added total": 0, "multi": [], "multi total" : 1}
    ]
    globalmulti = {"multi": [], "multi total": 1}

    randmod = 1 + attackroll_randmod*(random()*2 - 1) #random roll
    globalmulti["multi"].append(randmod)

    if ( random() < critchance ):
        crit = True
        globalmulti["multi"].append(critmulti)
    else:
        crit = False

    #calc total modifiers
    for element in range(len(ELEMENTS)):
        for addmod in elementalmodifiers[element]["added"]:
            elementalmodifiers[element]["added total"] += addmod
        for multimod in elementalmodifiers[element]["multi"]:
            elementalmodifiers[element]["multi total"] *= multimod
    for multimod in globalmulti["multi"]:
        globalmulti["multi total"] *= multimod

    #get outgoing dmg per element
    out_dmg = []
    for element in range(len(ELEMENTS)):
        d = (raw_dmg[element]+elementalmodifiers[element]["added total"])*elementalmodifiers[element]["multi total"]
        out_dmg.append(d) 

    #use appropriate resistance
    dmg = []
    for element in range(len(ELEMENTS)):
        d = int(out_dmg[element] * (1 - defendingBeast.RES[element]))
        dmg.append(d)

    total_dmg = sum(dmg)

    total_dmg = min( total_dmg, defendingBeast.HP )
    #resolve attack
    defendingBeast.HP -= total_dmg

    healthpercentage = ceil(total_dmg/defendingBeast.maxHP*100)
    print("> " + defendingBeast.nickname + " took " + str(total_dmg) + " (" + str(healthpercentage) + "%) damage! ", end="")
    if (crit):
        print("Critical hit! ")
    else:
        print("")

    if (defendingBeast.HP <= 0): #if the beast dies, attack ends immediately, so no secondary effects occur (only effects that take place after the attack)
        print("> " + defendingBeast.nickname + " died!")
        defendingBeast.death()
    else:
        #Secondary effects go here
        pass
    return