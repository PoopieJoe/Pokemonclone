from math import floor,ceil
from classes import Beast, Attack
from random import random
from fnmatch import fnmatch
import pygame
from globalconstants import *

def performattack(attackingBeast,defendingBeast,chained = False):
    attackresult = {
        "attacker": attackingBeast,
        "defender": defendingBeast,
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
        d = floor(out_dmg[element] * (1 - attackresult["defender"].RES[element]))
        attackresult["damage by element"].append(d)

    #sum up damage
    attackresult["damage total"] =  sum(attackresult["damage by element"])
    if (attackresult["damage total"] > 0): #if any damage was dealt, min is 1
        attackresult["damage total"] =  max(1,attackresult["damage total"])
        attackresult["damage total"] = min( attackresult["damage total"], attackresult["defender"].HP ) #total damage is hidden if target dies
    elif (attackresult["damage total"] < 0): #if any health was healed, min is 1
        attackresult["damage total"] =  min(-1,attackresult["damage total"])
    else:
        pass #don't do anything if total is exactly 0

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
            if ( fnmatch(effect, BURNNAME + "(*)") ):
                #fetch burn chance from string
                openparenpos = 4
                closeparenpos = len(effect)-1
                chance = float(effect[openparenpos+1:closeparenpos])
                if ( (random() < chance) and not [True for eff in attackresult["defender"].statuseffects if eff["name"] == BURNNAME]):
                    #apply burn
                    burndmg = attackresult["defender"].calcBurnDMG()
                    dmgpertick = burndmg[0]
                    ticksperdmg = burndmg[1]
                    
                    attackresult["defender"].addstatuseffect({"name":BURNNAME,"ticksperdmg":ticksperdmg,"dmgpertick":dmgpertick,"counter":ticksperdmg})
                    attackresult["secondary effects applied"].append(BURNNAME)
                    print("> "+ attackresult["defender"].nickname + " was burned!")

            elif ( fnmatch(effect, SLOWNAME + "_*(*)") ):
                #fetch slow chance and intensity from string
                underscorepos = effect.find('_')
                openparenpos = effect.find('(')
                closeparenpos = effect.find(')')
                duration = int(effect[underscorepos+1:openparenpos]) #duration in 1/6th turns
                chance = float(effect[openparenpos+1:closeparenpos])
                if ( (random() < chance) and not [True for eff in attackresult["defender"].statuseffects if (eff["name"] == SLOWNAME and eff["trackleft"] < duration*TURNTRACKER_LENGTH)]):
                    attackresult["defender"].addstatuseffect({"name":SLOWNAME,"duration":duration*TURNTRACKER_LENGTH/6,"trackleft":duration*TURNTRACKER_LENGTH/6})
 
    return attackresult

#Button actions
def backaction():
    print("This is where the back function should do something but I don't know how yet")
    return

def continueaction():
    try:
        #this lterally does nothing why did I type this
        return True
    except Exception:
        return False
    