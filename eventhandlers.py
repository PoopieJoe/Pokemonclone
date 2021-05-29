from math import floor,ceil
from classes import Beast, Attack
from random import random
from fnmatch import fnmatch
import pygame
import ui
from globalconstants import *

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

def performattack(scene,attackingBeast,chained = False):

    attackresult = {
        "attacker": attackingBeast,
        "defender": scene.beasts[attackingBeast.selected_attack[1]],
        "attack": attackingBeast.selected_attack[0],
        "success": False,
        "hit": False,
        "crit": False,
        "damage total": 0,
        "damage by element": [0,0,0,0],
        "secondary effects applied": [],
        "chain": {"type": "none", "value": 0}
    }

    if (chained): #chained attacks don't need to be printed again
        print("\n> " + attackingBeast.nickname + " used " + attackresult["attack"].name + " on " + attackresult["defender"].nickname + "!")
    
    if (attackresult["defender"].isalive == False):
        if (chained == None): #chained attacks just stop printing if they're dead
            print("> No target, the attack failed!")
        return attackresult
    else:
        attackresult["success"] = True

    #stuff that happens before the attack executes
    for effect in attackresult["attack"].effects:
        if ( fnmatch(effect, "Multihit_*") ):
            if (chained): #if we're already chaining just decrement counter
                attackresult["chain"]["value"] = chained - 1
            else:
                numhits = int(effect[len(effect)-1])
                attackresult["chain"] = {"type": "num_left", "value": numhits - 1}

    #determine hit
    if ( random() >= (attackresult["attack"].accuracy) ):
        print("> The attack missed!")
        return attackresult
    else:
        attackresult["hit"] = True

    #if hit, calculate dmg

    #get unmodified damage
    raw_physdmg = attackresult["attack"].power[0]*attackresult["attacker"].physATK
    raw_magdmg = [attackresult["attacker"].magATK*element for element in attackresult["attack"].power[1:]]
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
        attackresult["crit"] = True
        globalmulti["multi"].append(critmulti)
    else:
        attackresult["crit"] = False

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
    for element in range(len(ELEMENTS)):
        d = int(out_dmg[element] * (1 - attackresult["defender"].RES[element]))
        attackresult["damage by element"].append(d)

    #total damage is hidden if target dies
    attackresult["damage total"] = sum(attackresult["damage by element"])
    attackresult["damage total"] = min( attackresult["damage total"], attackresult["defender"].HP )

    #resolve attack
    attackresult["defender"].HP -= attackresult["damage total"]

    healthpercentage = ceil(attackresult["damage total"]/attackresult["defender"].maxHP*100)
    print("> " + attackresult["defender"].nickname + " took " + str(attackresult["damage total"]) + " (" + str(healthpercentage) + "%) damage! ", end="")
    if (attackresult["crit"]):
        print("Critical hit! ")
    else:
        print("")

    if (attackresult["defender"].HP <= 0): #if the beast dies, attack ends immediately, so no secondary effects occur (only effects that take place after the attack)
        attackresult["defender"].death()
    else:
        #Secondary effects go here
        for effect in attackresult["attack"].effects:
            if ( fnmatch(effect, "Burn(*)") ):
                #fetch burn chance from string
                openparenpos = 4
                closeparenpos = len(effect)-1
                chance = float(effect[openparenpos+1:closeparenpos])
                if ( (random() < chance) and not [True for effect in attackresult["defender"].statuseffects if effect["name"] == "Burn"]):
                    #apply burn
                    dmgpertick = attackresult["defender"].maxHP*BURNDMG*attackresult["defender"].SPE/scene.turnTrackerLength
                    ticksperdmg = max(1,floor(1/dmgpertick))
                    dmgpertick = max(1,dmgpertick)
                    attackresult["defender"].addstatuseffect({"name":"Burn","ticksperdmg":ticksperdmg,"dmgpertick":dmgpertick,"counter":ticksperdmg})
                    attackresult["secondary effects applied"].append("Burn")
                    print("> "+ attackresult["defender"].nickname + " was burned!")
                
 
    return attackresult