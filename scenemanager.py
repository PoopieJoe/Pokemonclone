from classes import Beast, Flag, Attack, getAttack
from math import floor,ceil
from random import shuffle
from fnmatch import fnmatch
from random import random,shuffle
from globalconstants import *
import classes as c
import eventhandlers as evth

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
                slot.beast.setflag(FLAG_CHOOSEATTACK)
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
        priority_order = [FLAG_CHOOSEATTACK,FLAG_EXECUTEATTACK]
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
            if (flag_name == FLAG_CHOOSEATTACK):
                self.state = "Choose attack"
            elif (flag_name == FLAG_EXECUTEATTACK):
                self.state = "Execute attack"
            else:
                self.state = "Idle"

    ###################################
    # COMBAT
    ###################################

    def processattack(self):
        active_slot = self.active_slot
        if (active_slot.beast.getflag(FLAG_EXECUTEATTACK)):
            attack = active_slot.beast.selected_attack.atk
            defenderlist = active_slot.beast.selected_attack.slots

            print("\n> " + active_slot.beast.nickname + " used " + attack.name + " on " + " and ".join([slot.beast.nickname for slot in active_slot.beast.selected_attack.slots]) + "!")

            numhits = 1
            for flag in attack.flags:
                if (flag["name"] == MULTIHITNAME):
                    numhits = flag["value"]

            
            shuffle(defenderlist)   #random order #TODO (should we sort this by speed?)
            for target in defenderlist: #repeat for every target
                #chain by ID
                curattack = attack
                while True:
                    for _ in range(0,numhits): #repeat if multihit
                        #perform next attack and append to output
                        result = self.attackhit(active_slot.beast,target.beast,curattack)
                        self.attackresult.append( result ) #append to output

                    curattack = self.getChainAttack(curattack) #get next attack in chain
                    if curattack == None:
                        break
                    
            self.attackDone()

        else:
            raise Exception(active_slot.beast.nickname + " has no attack selected!")
        return self.attackresult

    def attackDone(self):
            # clear flags and selected attack (is the latter even neccesary?)
            # (yes it is used to check if we're moving to attack, since track position is used to check if we shoud set the flag)
            self.active_slot.beast.clearflag(FLAG_EXECUTEATTACK)
            self.active_slot.beast.selected_attack = c.SelectedAtk(None,-1)

    def getChainAttack(self,attack:Attack):
        if (attack.chainID >= 0):
            return getAttack(attack.chainID)
        else:
            return None

    def attackhit(self,attackerbeast:Beast,defenderbeast:Beast,atk:Attack):        
        attackresult = {
            "attacker": attackerbeast,
            "defender": defenderbeast,
            "attack": atk,
            "success": False,
            "hit": False,
            "crit": False,
            "damage total": 0,
            "damage by element": {
                PHYSNAME: 0,
                HEATNAME: 0,
                COLDNAME: 0,
                SHOCKNAME: 0
            },
            "secondary effects": []
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
            {"added": [], "added total": 0, "multi": [], "multi total" : 1}, # PHYS modifiers
            {"added": [], "added total": 0, "multi": [], "multi total" : 1}, # HEAT modifiers
            {"added": [], "added total": 0, "multi": [], "multi total" : 1}, # COLD modifiers
            {"added": [], "added total": 0, "multi": [], "multi total" : 1}  # SHOCK modifiers
        ]
        globalmulti = {"multi": [], "multi total": 1} # global modifiers

        randmod = 1 + ATTACKROLL_RANDMOD*(random()*2 - 1) #random roll
        globalmulti["multi"].append(randmod)

        if ( random() < CRITCHANCE ):
            attackresult["crit"] = True
            globalmulti["multi"].append(CRITMULTI)
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
            attackresult["damage by element"][ELEMENTS[element]] = d

        #sum up damage
        for element in ELEMENTS:
            attackresult["damage total"] += attackresult["damage by element"][element]
        attackresult["damage total"] = evth.rounddmg(attackresult["damage total"])

        attackresult["damage total"] = min( attackresult["damage total"], attackresult["defender"].HP ) #total damage is hidden if target dies or is healed to full

        #resolve attack
        attackresult["defender"].HP -= attackresult["damage total"]

        healthpercentage = ceil(attackresult["damage total"]/attackresult["defender"].maxHP*100)
        print("> " + attackresult["defender"].nickname + " took " + str(attackresult["damage total"]) + " (" + str(healthpercentage) + "%) damage! ", end="")
        if (attackresult["crit"]):
            print("Critical hit! ")
        else:
            print("")

        print(">> Damage breakdown: " + evth.getdmgbreakdownstring(attackresult["damage by element"]))

        if (attackresult["defender"].HP <= 0): #if the beast dies, attack ends immediately, so no secondary effects occur (only effects that take place after the attack)
            attackresult["defender"].death()
        else:
            #Secondary effects go here

            #first effects from the attack
            for effect in attackresult["attack"].effects:
                if random() < effect["chance"]:
                    if ( effect["name"] == BURNNAME ):
                        if ( not [True for eff in attackresult["defender"].statuseffects if eff["name"] == BURNNAME] ):
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
                            attackresult["secondary effects"].append(burnstatus)
                            print("> "+ attackresult["defender"].nickname + " was burned!")

                    elif ( effect["name"] == SLOWNAME ):
                        if ( not [True for eff in attackresult["defender"].statuseffects if (eff["name"] == SLOWNAME and eff["trackleft"] < effect["value"]*TURNTRACKER_LENGTH)]):
                            slowstatus = {
                                "name":SLOWNAME,
                                "duration":effect["value"]*TURNTRACKER_LENGTH*SLOWBASEDURATION,
                                "trackleft":effect["value"]*TURNTRACKER_LENGTH*SLOWBASEDURATION
                            }
                            attackresult["defender"].addstatuseffect(slowstatus)
                            attackresult["secondary effects"].append(slowstatus)
                            print("> "+ attackresult["defender"].nickname + " was slowed!")
            
            #second effects from contact moves
            for effect in attackresult["defender"].equipmenteffects:
                if (random() < effect["chance"]):
                    if (effect["name"] == "Reflect"):
                        #attacker takes fraction of dealt damage (of the same type as taken by the defender)
                        reflectresult = {   
                            "name":REFLECTNAME,
                            "damage by element": {
                                PHYSNAME: 0,
                                HEATNAME: 0,
                                COLDNAME: 0,
                                SHOCKNAME: 0
                            },
                            "damage total": 0
                        }

                        for element in ELEMENTS:
                            reflectresult["damage by element"][element] = evth.rounddmg(attackresult["damage by element"][element]*effect["value"]*REFLECTBASEVAL)
                            reflectresult["damage total"] += reflectresult["damage by element"][element]

                        attackresult["attacker"].HP -= reflectresult["damage total"]

                        attackresult["secondary effects"].append(reflectresult)
                        print("> " + attackresult["defender"].nickname + " reflected " + str(reflectresult["damage total"])  + " (" + str(round(reflectresult["damage total"]/attackresult["attacker"].maxHP*100)) + "%) dmg back to " + attackresult["attacker"].nickname)
                        print(">> Damage breakdown: " + evth.getdmgbreakdownstring(reflectresult["damage by element"]))


        return attackresult

    ###################################
    # STATE UPDATE
    ###################################

    def tick(self):
        #game can only tick if no events need to be processed
        if (len(self.raisedFlags) > 0 or self.state != "Idle"):
            return False

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

        #set flags
        for slot in self.slots:
            beast = slot.beast
            if (beast.isalive):
                if (beast.selected_attack.atk != None): #has any move selected (moving to attack)
                    if (slot.turntracker >= self.turnTrackerLength/2): #check if tt exceeds threshold
                        beast.setflag(FLAG_EXECUTEATTACK)
                else: #no move selected (moving from attack)
                    if (slot.turntracker >= self.turnTrackerLength): #exceeded turn tracker length
                        beast.setflag(FLAG_CHOOSEATTACK)
                        slot.turntracker = 0
        
        return True
