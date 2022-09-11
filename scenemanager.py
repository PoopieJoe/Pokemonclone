from __future__ import annotations
from math import floor,ceil
from random import shuffle
from fnmatch import fnmatch
from random import random,shuffle
from xmlrpc.client import Boolean
from globalconstants import *
import classes as c

class FlagListItem:
    def __init__(self, flag:c.Flag, slot:c.Slot):
        self.flag = flag
        self.slot = slot

class Scene:
    slots: list[c.Slot]
    raisedFlags: list[FlagListItem]
    flags: list[list[FlagListItem]]
    attackresult: list[dict]
    active_flag: FlagListItem
    active_slot: c.Slot

    def __init__(self,format:str):
        self.slots = []
        self.turnTrackerLength = TURNTRACKER_LENGTH
        self.flags = [[]]


        self.state = SCENESTATES.IDLE
        self.state_changed = False

        self.setformat(format)

        self.active_flag = None
        self.active_slot = None
        self.raisedFlags = []
        self.attackresult = []
        
    def setformat(self,format:str):
        if BATTLEFORMATS.contains(format):
            self.battleformat = format
            return True
        else:
            return False

    def getformat(self) -> str:
        return self.battleformat

    def addBeast(self, beast:c.Beast, team:c.Team):
        newslot = c.Slot(beast,team)
        newslot.num = len(self.slots)
        self.slots.append(newslot)
    
    def removeBeast(self, slot: c.Slot):
        self.slots.pop(slot)
    
    def setupBattle(self):
        for slot in self.slots:
            if (slot.beast != None):
                slot.beast.clearALLflags()
                slot.beast.isalive = True
                slot.beast.HP = 1#slot.beast.maxHP
                slot.beast.setflag(FLAG_CHOOSEATTACK)
            slot.turntracker = 0

    ###################################
    # FLAG AND EVENT MANAGEMENT
    ###################################

    def setstate(self,state:str):
        if not state == self.state:
            self.state_changed = True
            self.state = state
        return

    def getstate(self) -> str:
        return self.state

    def statechanged(self) -> bool:
        if self.state_changed:
            self.state_changed = False
            return True
        else:
            return False

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

    def noactiveflag(self):
        return (self.active_flag == None)

    def noflags(self):
        return ((self.active_flag == None) and (len(self.raisedFlags) == 0))

    def clearactiveflag(self):
        self.active_flag = None

    def popflag(self):
        if ((self.active_flag == None) and (len(self.raisedFlags) > 0)):
            self.active_flag = self.raisedFlags.pop(0)
            flag_name = self.active_flag.flag.type
            self.active_slot = self.active_flag.slot
            if (flag_name == FLAG_CHOOSEATTACK):
                self.setstate(SCENESTATES.CHOOSEATTACK)
            elif (flag_name == FLAG_EXECUTEATTACK):
                self.setstate(SCENESTATES.EXECUTEATTACK)
            else:
                self.setstate(SCENESTATES.IDLE)


    def selectattack(self,atk:c.Attack,beast:c.Beast=None):
        if beast == None:
            beast = self.active_slot.beast
        beast.selected_attack.setattack(atk)
    
    def selecttargets(self,slots:list[c.Slot],beast:c.Beast=None):
        if beast == None:
            beast = self.active_slot.beast
        beast.selected_attack.setslots(slots)

    ###################################
    # COMBAT
    ###################################

    def processattack(self):
        self.attackresult = [] # clear previous results
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
            self.active_slot.beast.selected_attack = c.SelectedAtk(None,None)

    def getChainAttack(self,attack:c.Attack):
        if (attack.chainID >= 0):
            return c.getAttack(attack.chainID)
        else:
            return None

    def attackhit(self,attackerbeast:c.Beast,defenderbeast:c.Beast,atk:c.Attack):        
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
        attackresult["damage total"] = rounddmg(attackresult["damage total"])

        attackresult["damage total"] = min( attackresult["damage total"], attackresult["defender"].HP ) #total damage is hidden if target dies or is healed to full

        #resolve attack
        attackresult["defender"].HP -= attackresult["damage total"]

        healthpercentage = ceil(attackresult["damage total"]/attackresult["defender"].maxHP*100)
        print("> " + attackresult["defender"].nickname + " took " + str(attackresult["damage total"]) + " (" + str(healthpercentage) + "%) damage! ", end="")
        if (attackresult["crit"]):
            print("Critical hit! ")
        else:
            print("")

        print(">> Damage breakdown: " + getdmgbreakdownstring(attackresult["damage by element"]))

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
                            reflectresult["damage by element"][element] = rounddmg(attackresult["damage by element"][element]*effect["value"]*REFLECTBASEVAL)
                            reflectresult["damage total"] += reflectresult["damage by element"][element]

                        attackresult["attacker"].HP -= reflectresult["damage total"]

                        attackresult["secondary effects"].append(reflectresult)
                        print("> " + attackresult["defender"].nickname + " reflected " + str(reflectresult["damage total"])  + " (" + str(round(reflectresult["damage total"]/attackresult["attacker"].maxHP*100)) + "%) dmg back to " + attackresult["attacker"].nickname)
                        print(">> Damage breakdown: " + getdmgbreakdownstring(reflectresult["damage by element"]))


        return attackresult

    ###################################
    # STATE UPDATE
    ###################################

    def run(self):
        if (self.noflags()):
            self.fetchFlags()

        if self.noactiveflag():
            self.popflag()

        #change gamestate according to state
        if (self.getstate() == SCENESTATES.EXECUTEATTACK):
            if (self.active_slot.beast.selected_attack.atk != None):
                self.processattack()
            else:
                self.attackDone()
        elif (len(self.raisedFlags) == 0 and self.getstate() == SCENESTATES.IDLE):
            self.tick()

        #check win/lose condition
        if self.getformat() == BATTLEFORMATS.FREEFORALL:
            # Last man standing
            livingbeasts = [slot.beast for slot in self.slots if slot.beast.isalive]
            deadbeasts = [slot.beast for slot in self.slots if not slot.beast.isalive]
            if len(livingbeasts) == 1:
                self.rankings = {"winners":livingbeasts,"losers":deadbeasts}
                self.setstate(SCENESTATES.DONE)


    def tick(self):
        #game can only tick if no events need to be processed
        if (len(self.raisedFlags) > 0 or self.getstate() != SCENESTATES.IDLE):
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

        #check if anyone indirectly died last tick (so not through attackhit())
        for slot in self.slots:
            beast = slot.beast
            if (beast.HP <= 0 and beast.isalive):
                beast.death()

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


def rounddmg(dmg:float) -> int:
    if (dmg > 0): #if any damage was dealt, min is 1
        dmg =  max(1,dmg)
    elif (dmg < 0): #if any health was healed, min is 1
        dmg =  min(-1,dmg)
    else:
        pass #don't do anything if total is exactly 0

    return int(dmg)

def getdmgbreakdownstring(dmgbyelement:dict) -> list:
    stringlist = []
    for element in ELEMENTS:
        if (dmgbyelement[element] > 0):
            stringlist.append(element + ": " + str(dmgbyelement[element]))
    return ", ".join(stringlist)

def continueaction():
    try:
        #this lterally does nothing why did I type this
        return True
    except Exception:
        return False