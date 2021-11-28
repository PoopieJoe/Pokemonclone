from classes import Beast, Flag, Attack
from math import floor,ceil
from itertools import chain
from random import shuffle
from fnmatch import fnmatch
from random import random,shuffle
from time import sleep
from globalconstants import *
import classes as c

class Team:
    def __init__(self):
        self.beasts = []
        self.subs = []
        self.name = ""

class Slot:
    def __init__(self, beast:Beast, team:int):
        self.num = -1
        self.beast = beast
        self.team = team
        self.turntracker = 0

class FlagListItem:
    def __init__(self, flag:Flag, slot:Slot):
        self.flag = flag
        self.slot = slot

class Scene:
    def __init__(self):
        self.slots = []
        self.turnTrackerLength = TURNTRACKER_LENGTH
        self.flags = [[]]

        self.state = "Idle"
        self.active_flag = None
        self.raisedFlags = []
        self.attackresult = []

    def addBeast(self, beast, team):
        newslot = Slot(beast,team)
        newslot.num = len(self.slots)
        self.slots.append(newslot)
    
    def removeBeast(self, slot: Slot):
        self.slots.pop(slot)
    
    def setupBattle(self):
        for slot in self.slots:
            if (slot.beast != None):
                slot.beast.clearALLflags()
                slot.beast.isalive = True
                slot.beast.HP = slot.beast.maxHP
                slot.beast.setflag("choose_attack")
            slot.turntracker = 0

    def printScene(self):
        #TODO remake this
        # print("\n###########################################")
        # if (self.beasts[1].isalive or self.beasts[2].isalive):
        #     print("Team A: ")
        #     if (self.beasts[1].isalive):
        #         print("  Slot 1: " + self.beasts[1].nickname.ljust(16," ") + str(self.beasts[1].HP).ljust(3," ") + "/" + str(self.beasts[1].maxHP).ljust(3," ") + " HP (" + str(round(self.beasts[1].HP/self.beasts[1].maxHP*100)).ljust(3," ") + "%)")
        #     if (self.beasts[2].isalive):
        #         print("  Slot 2: " + self.beasts[2].nickname.ljust(16," ") + str(self.beasts[2].HP).ljust(3," ") + "/" + str(self.beasts[2].maxHP).ljust(3," ") + " HP (" + str(round(self.beasts[2].HP/self.beasts[2].maxHP*100)).ljust(3," ") + "%)")
        # if (self.beasts[3].isalive or self.beasts[4].isalive):
        #     print("Team B: ")
        #     if (self.beasts[3].isalive):
        #         print("  Slot 3: " + self.beasts[3].nickname.ljust(16," ") + str(self.beasts[3].HP).ljust(3," ") + "/" + str(self.beasts[3].maxHP).ljust(3," ") + " HP (" + str(round(self.beasts[3].HP/self.beasts[3].maxHP*100)).ljust(3," ") + "%)")
        #     if (self.beasts[4].isalive):
        #         print("  Slot 4: " + self.beasts[4].nickname.ljust(16," ") + str(self.beasts[4].HP).ljust(3," ") + "/" + str(self.beasts[4].maxHP).ljust(3," ") + " HP (" + str(round(self.beasts[4].HP/self.beasts[4].maxHP*100)).ljust(3," ") + "%)")
        # print("###########################################")
        return

    ###################################
    # FLAG AND EVENT MANAGEMENT
    ###################################

    def setstate(self,state:str):
        self.state = state
        return

    def fetchFlags(self):
        #check for raised event flags and sort flags
        #rules: from first resolved to last resolved: choose move, attacks
        #       multiple flags of the same type are resolved in random order
        priority_order = ["choose_attack","execute_attack"]
        segmented_flaglist = [[] for _ in priority_order]
        for slot in self.slots:
            for flag in slot.beast.flags:
                if (flag.israised()):
                    priority = priority_order.index(flag.type)
                    segmented_flaglist[priority].append(FlagListItem(flag,slot))

        #Shuffle flags with same priority and concatanate them on the total list
        for segment in segmented_flaglist:
            shuffle(segment)
            self.raisedFlags.extend(segment)
        return

    def noflags(self):
        return ((self.active_flag == None) and (len(self.raisedFlags) == 0))

    def popflag(self):
        if ((self.active_flag == None) and (len(self.raisedFlags) > 0)):
            self.active_flag = self.raisedFlags.pop(0)
            flag_name = self.active_flag.flag.type
            self.active_slot = self.active_flag.slot
            if (flag_name == "choose_attack"):
                self.state = "Choose attack"
            elif (flag_name == "execute_attack"):
                attackresult = []
                self.state = "Execute attack"
            else:
                self.state = "Idle"

    ###################################
    # COMBAT AND TICKS
    ###################################

    def processattack(self):
        active_slot = self.active_slot
        if (active_slot.beast.getflag("execute_attack")):
            attack = active_slot.beast.selected_attack.atk
            defenderlist = active_slot.beast.selected_attack.slots

            #TODO this is different for multitarget attack
            print("\n> " + active_slot.beast.nickname + " used " + attack.name + " on " + " and ".join([slot.beast.nickname for slot in active_slot.beast.selected_attack.slots]) + "!")

            numhits = 1
            for effect in attack.effects:
                if (effect["name"] == MULTIHITNAME):
                    numhits = effect["value"]

            
            shuffle(defenderlist)   #random order
            for target in defenderlist: #repeat for every target
                for _ in range(0,numhits): #repeat if multihit
                    #perform next attack and append to output
                    result = self.attackhit(active_slot.beast,target.beast,attack)
                    self.attackresult.append( result ) #append to output

            #TODO: chain by ID

            #clear flags and selected attack (is the latter even neccesary?)
            active_slot.beast.clearflag("execute_attack")
            active_slot.beast.selected_attack = c.SelectedAtk(None,-1)
        else:
            raise Exception(self.nickname + " has no attack selected!")
        return self.attackresult

    def attackhit(self,attackerbeast:Beast,defenderbeast:Beast,atk:Attack):        
        attackresult = {
            "attacker": attackerbeast,
            "defender": defenderbeast,
            "attack": atk,
            "success": False,
            "hit": False,
            "crit": False,
            "damage total": 0,
            "damage by element": [0,0,0,0],
            "secondary effects applied": []
        }          
        
        if (attackresult["defender"].isalive == False):
            print("> No target, the attack failed!")
            return attackresult
        else:
            attackresult["success"] = True

        #stuff that happens before the attack executes
        for effect in attackresult["attack"].effects:
            pass

        #determine hit
        if ( random() >= (attackresult["attack"].accuracy) ):
            print("> The attack on " + defenderbeast.nickname + " missed!")
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
                if ( effect["name"] == BURNNAME ):
                    if ( (random() < effect["chance"]) and not [True for eff in attackresult["defender"].statuseffects if eff["name"] == BURNNAME]):
                        #apply burn
                        burndmg = attackresult["defender"].calcBurnDMG()
                        dmgpertick = burndmg[0]
                        ticksperdmg = burndmg[1]
                        
                        burnstatus = {
                            "name":BURNNAME,
                            "ticksperdmg":ticksperdmg,
                            "dmgpertick":dmgpertick,
                            "counter":ticksperdmg
                        }
                        attackresult["defender"].addstatuseffect(burnstatus)
                        attackresult["secondary effects applied"].append(BURNNAME)
                        print("> "+ attackresult["defender"].nickname + " was burned!")

                elif ( effect["name"] == SLOWNAME ):
                    if ( (random() < effect["chance"]) and not [True for eff in attackresult["defender"].statuseffects if (eff["name"] == SLOWNAME and eff["trackleft"] < effect["value"]*TURNTRACKER_LENGTH)]):
                        slowstatus = {
                            "name":SLOWNAME,
                            "duration":effect["value"]*TURNTRACKER_LENGTH/6,
                            "trackleft":effect["value"]*TURNTRACKER_LENGTH/6
                        }
                        attackresult["defender"].addstatuseffect(slowstatus)
                        attackresult["secondary effects applied"].append(SLOWNAME)
                        print("> "+ attackresult["defender"].nickname + " was slowed!")

        return attackresult

    def tick(self):
        #game can only tick if no events need to be processed
        if (len(self.raisedFlags) > 0 or self.state != "Idle"):
            return False
        sleep(1/30) #worlds shittiestly programmed framerate

        #check relevant status flags
        for slot in self.slots:
            if (slot.beast.isalive):
                beast = slot.beast
                status_ended = []
                for n,status in enumerate(beast.statuseffects):
                    if ( fnmatch(status["name"], BURNNAME) ):
                        status["counter"] -= 1
                        if (status["counter"] == 0):
                            #take dmg
                            beast.HP = beast.HP - status["dmgpertick"]

                            #determine new damage and tick values for next dmg instance in case hp total changes during burn effect
                            burndmg = beast.calcBurnDMG()
                            status["dmgpertick"] = burndmg[0]
                            status["ticksperdmg"] = burndmg[1]
                            status["counter"] = status["ticksperdmg"]

                    elif ( fnmatch(status["name"], SLOWNAME) ):
                        if (status["duration"] == status["trackleft"]):
                            beast.SPE *= SLOWMOD
                        elif (status["trackleft"] <= 0):
                            beast.SPE /= SLOWMOD
                            status_ended.append(n) #queue this effect for removal
                        status["trackleft"] -=  beast.SPE

                #remove effects that have ended
                for index in status_ended:
                    beast.statuseffects.pop(index) #remove status

        #check if anyone died last tick
        for slot in self.slots:
            beast = slot.beast
            if (beast.HP <= 0 and beast.isalive):
                beast.death()
                print("> " + slot.beast.nickname + " died!")

        #increment turn tracker
        for slot in self.slots:
            beast = slot.beast
            if (beast.isalive):
                if ((slot.turntracker < TURNTRACKER_LENGTH/2) and (slot.turntracker + beast.SPE > TURNTRACKER_LENGTH/2)):
                    slot.turntracker = TURNTRACKER_LENGTH/2
                else:
                    slot.turntracker = slot.turntracker + beast.SPE

        #set flags TODO fix
        for slot in self.slots:
            beast = slot.beast
            if (beast.isalive):
                #check if tt exceeds threshold
                if (beast.selected_attack.atk != None): #has any move selected (moving to attack)
                    if (slot.turntracker >= self.turnTrackerLength/2):
                        beast.setflag("execute_attack")
                else: #no move selected (moving from attack)
                    if (slot.turntracker >= self.turnTrackerLength): #exceeded turn tracker length
                        beast.setflag("choose_attack")
                        slot.turntracker = 0
        
        return True