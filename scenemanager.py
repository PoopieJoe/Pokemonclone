from classes import Beast, Attack
from math import floor,ceil
from itertools import chain
from random import shuffle
from fnmatch import fnmatch
from globalconstants import *

class Scene:
    def __init__(self):
        self.beasts = [None,None,None,None,None]
        self.turnTracker = [0,0,0,0,0]
        self.turnTrackerLength = 20000
        self.flags = [[]]

    def addBeast(self, beast, slot):
        self.beasts[slot] = beast
    
    def removeBeast(self, beast, slot):
        self.beasts[slot] = None
    
    def setupBattle(self):
        for beast in self.beasts[1:]:
            if (beast != None):
                beast.clearALLflags()
                beast.isalive = True
                beast.HP = beast.maxHP
                beast.setflag(1)
                
        self.turnTracker = [0,0,0,0,0]

    def printScene(self):
        print("\n###########################################")
        if (self.beasts[1].isalive or self.beasts[2].isalive):
            print("Team A: ")
            if (self.beasts[1].isalive):
                print("  Slot 1: " + self.beasts[1].nickname.ljust(16," ") + str(self.beasts[1].HP).ljust(3," ") + "/" + str(self.beasts[1].maxHP).ljust(3," ") + " HP (" + str(round(self.beasts[1].HP/self.beasts[1].maxHP*100)).ljust(3," ") + "%)")
            if (self.beasts[2].isalive):
                print("  Slot 2: " + self.beasts[2].nickname.ljust(16," ") + str(self.beasts[2].HP).ljust(3," ") + "/" + str(self.beasts[2].maxHP).ljust(3," ") + " HP (" + str(round(self.beasts[2].HP/self.beasts[2].maxHP*100)).ljust(3," ") + "%)")
        if (self.beasts[3].isalive or self.beasts[4].isalive):
            print("Team B: ")
            if (self.beasts[3].isalive):
                print("  Slot 3: " + self.beasts[3].nickname.ljust(16," ") + str(self.beasts[3].HP).ljust(3," ") + "/" + str(self.beasts[3].maxHP).ljust(3," ") + " HP (" + str(round(self.beasts[3].HP/self.beasts[3].maxHP*100)).ljust(3," ") + "%)")
            if (self.beasts[4].isalive):
                print("  Slot 4: " + self.beasts[4].nickname.ljust(16," ") + str(self.beasts[4].HP).ljust(3," ") + "/" + str(self.beasts[4].maxHP).ljust(3," ") + " HP (" + str(round(self.beasts[4].HP/self.beasts[4].maxHP*100)).ljust(3," ") + "%)")
        print("###########################################")

    def tick(self):
        #check relevant status flags
        for slot, beast in enumerate(self.beasts[1:],start=1):
            if (beast.isalive):
                status_ended = []
                for n,status in enumerate(beast.statuseffects):
                    if ( fnmatch(status["name"], BURNNAME) ):
                        status["counter"] -= 1
                        if (status["counter"] == 0):
                            #take dmg
                            beast.HP = beast.HP - status["dmgpertick"]

                            #determine new damage and tick values for next dmg instance in case hp total or speed changes during burn effect
                            dmgpertick = BURNDMG*beast.maxHP*beast.SPE/self.turnTrackerLength
                            status["ticksperdmg"] = max(1,floor(1/dmgpertick))
                            status["dmgpertick"] = max(1,dmgpertick)
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

        #increment turn tracker
        for slot, beast in enumerate(self.beasts[1:],start=1):
            self.turnTracker[slot] = self.turnTracker[slot] + beast.SPE

        #check if anyone died last tick
        for slot, beast in enumerate(self.beasts[1:],start=1):
            if (beast.HP <= 0 and beast.isalive):
                beast.death()
                print("> " + beast.nickname + " died!")

        #set flags
        for slot, beast in enumerate(self.beasts[1:],start=1):
            if (beast.isalive):
                #check if tt exceeds threshold
                if (beast.selected_attack[0] != None): #has any move selected (moving to attack)
                    if (self.turnTracker[slot] >= self.turnTrackerLength/2):
                        self.beasts[slot].setflag(0)
                else: #no move selected (moving from attack)
                    if (self.turnTracker[slot] >= self.turnTrackerLength): #exceeded turn tracker length
                        self.beasts[slot].setflag(1)
                        self.turnTracker[slot] = 0

def fetchFlags(scene):
    #check for raised event flags and sort flags
    #rules: from first resolved to last resolved: choose move, attacks
    #       multiple flags of the same type are resolved in random order
    priority_order = ["choose_attack","execute_attack"]
    segmented_flaglist = [[] for x in priority_order]
    for slot, beast in enumerate(scene.beasts[1:],start=1):
        for flag in beast.flags:
            if (flag[1]):
                priority = priority_order.index(flag[0])
                segmented_flaglist[priority].append([priority_order[priority],slot])

    #Shuffle flags with same priority
    for segment in segmented_flaglist:
        shuffle(segment)

    #concatenate segments
    flaglist = []
    for segment in segmented_flaglist:
        for flag in segment:
            flaglist.append(flag)
    
    return flaglist
