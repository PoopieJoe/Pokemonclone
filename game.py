from random import random
from math import floor
from classes import *
from printdetails import printFullBeastStatus
from scenemanager import Scene
from random import shuffle

Elements = ["none","physical","heat","cold","shock"]
attackroll_randmod = 0.1 #attacks deal randomly between 90% and 110% dmg
critchance = 0.05 #5% critchance

def moveselect(scene,slot):
    scene.printScene()
    beast = scene.beasts[slot]
    #show status
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
        selected_slot = int(input("Select target slot: ").strip())

    print("> " + beast.name + " (Slot " + str(slot) + ") will use " + selected_move.name + " on " + scene.beasts[selected_slot].name + " (Slot " + str(selected_slot) + ")!")

    beast.selected_attack = [selected_move,selected_slot]
    scene.turnTracker[slot] = 0
    beast.clearflag(1)
    return

def performattack(scene,slot):
    attackingBeast = scene.beasts[slot]
    defendingBeast = scene.beasts[attackingBeast.selected_attack[1]]
    attack = attackingBeast.selected_attack[0]

    print("\n> " + attackingBeast.name + " used " + attack.name + " on " + defendingBeast.name + "!")

    #determine hit
    if ( random() >= (attack.accuracy) ):
        print("> The attack missed!")
        attackingBeast.selected_attack = [Attack(),0]
        attackingBeast.clearflag(0)
        return

    #if hit, calculate dmg

    #get modifiers
    modifierList = []
    randmod = random()*2*attackroll_randmod + 1 - attackroll_randmod #random roll
    modifierList.append(randmod)

    if ( random() < critchance ):
        crit = True
        critmod = 1 + 0.5
    else:
        crit = False
        critmod = 1
    modifierList.append(critmod)

    #calc total modifier
    totalModifier = 1
    for modifier in modifierList:
        totalModifier *= modifier

    #use appropriate resistance
    if (attack.element == "physical"):
        dmg = round(attackingBeast.ATK * attack.power * 100 / defendingBeast.DEF * totalModifier)
    else:
        if (attack.element == "heat"):
            resistance = defendingBeast.heatRES
        elif (attack.element == "cold"):
            resistance = defendingBeast.coldRES
        elif (attack.element == "shock"):
            resistance = defendingBeast.shockRES
        dmg = min( round(attackingBeast.ATK * attack.power * (1-resistance) * totalModifier) , defendingBeast.HP)

    #resolve attack
    defendingBeast.HP -= dmg

    healthpercentage = floor(dmg/defendingBeast.maxHP*100)
    print("> " + defendingBeast.name + " took " + str(dmg) + " (" + str(healthpercentage) + "%) damage! ", end="")
    if (crit):
        print("Critical hit! ")
    else:
        print("")

    if (defendingBeast.HP <= 0): #if the beast dies, attack ends immediately, so no secondary effects occur (only effects that take place after the attack)
        print("> " + defendingBeast.name + " died!")
        defendingBeast.death()
    else:
        #Secondary effects go here
        pass
    attackingBeast.selected_attack = [Attack(),0]
    attackingBeast.clearflag(0)
    return

Attack1 = Attack(name="Slam",power=1.00,element="physical",accuracy=0.90)
Attack2 = Attack(name="Ray of Fire",power=0.80,element="heat",accuracy=1.00)

Equipment1 = Equipment(name="Metal chestplate",attacks=[Attack1,Attack2],statbonuses=[("maxHP",+50),("DEF",+20),("shockRES",-0.30)])

Beast1 = Beast("Greg", maxHP = 110, ATK = 100, DEF = 100, heatRES = 0.30, coldRES = -0.20, shockRES = 0, SPE = 100)
Beast1.equipItem(Equipment1)

Beast2 = Beast("Micheala", maxHP = 92, ATK = 100, DEF = 100, heatRES = 0, coldRES = 0, shockRES = 0, SPE = 105)
Beast2.equipItem(Equipment1)

scene = Scene()
scene.addBeast(beast = Beast1,slot = 1)
scene.addBeast(beast = Beast2,slot = 3)

scene.setupBattle()
battle_active = True
winner = 0
while (battle_active):
    #check for raised flags and sort flags
    #rules: from first resolved to last resolved: choose move, attacks
    #       multiple flags of the same type are resolved in random order
    choose_attack_list = []
    execute_attack_list = []
    flaglist = [choose_attack_list,execute_attack_list]
    for slot, beast in enumerate(scene.beasts[1:],start=1):
        for flag in beast.flags:
            if (flag[1] == True):
                if (flag[0] == "choose_attack"):
                    choose_attack_list.append(slot)
                elif (flag[0] == "execute_attack"):
                    execute_attack_list.append(slot)

    #Shuffle flags with same priority
    for sublist in flaglist:
        shuffle(sublist)

    #resolve flags
    for flag_id, sublist in enumerate(flaglist,start=0):
        resolve_function = [moveselect,performattack][flag_id]
        for slot in sublist:
            resolve_function(scene,slot)
    
    #check if only one teams beasts are remaining (that teams wins, and the battle ends)
    if (not (scene.beasts[1].isalive or scene.beasts[2].isalive)):
        battle_active = False
        winner = "B"
    elif (not (scene.beasts[3].isalive or scene.beasts[4].isalive)):
        battle_active = False
        winner = "A"

    scene.tick()

scene.printScene()
print("Team " + winner + " wins!")