from classes import Beast, Flag, Attack
from math import floor,ceil
from itertools import chain
from random import shuffle
from fnmatch import fnmatch
from time import sleep
from globalconstants import *

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
        self.active_beast = None
        self.active_flag = None
        self.raisedFlags = []
        self.attackresult = []

    def addBeast(self, beast, team):
        newslot = Slot(beast,team)
        newslot.num = len(self.slots)
        self.slots.append(newslot)
    
    def removeBeast(self, slot):
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

    def setstate(self,state):
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