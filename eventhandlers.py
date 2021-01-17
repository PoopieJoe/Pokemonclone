from math import floor,ceil
from classes import Beast, Attack
from random import random

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
        dmg = round(attackingBeast.ATK * attack.power * (1-resistance) * totalModifier)
    dmg = min( dmg, defendingBeast.HP )
    #resolve attack
    defendingBeast.HP -= dmg

    healthpercentage = ceil(dmg/defendingBeast.maxHP*100)
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