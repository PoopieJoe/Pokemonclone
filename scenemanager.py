from classes import Beast, Attack
from math import floor,ceil

class Scene:
    def __init__(self):
        self.beasts = [Beast(),Beast(),Beast(),Beast(),Beast()]
        self.turnTracker = [0,0,0,0,0]
        self.turnTrackerLength = 20000
        self.flags = [[]]

    def addBeast(self, beast, slot):
        self.beasts[slot] = beast
    
    def removeBeast(self, beast, slot):
        self.beasts[slot] = Beast()
    
    def setupBattle(self):
        for beast in self.beasts:
            beast.clearALLflags()
            if (beast.name == Beast().name):
                beast.isalive = False
            else:
                beast.isalive = True
                beast.HP = beast.maxHP
                beast.setflag(1)
                
        self.turnTracker = [0,0,0,0,0]

    def printScene(self):
        print("\n###########################################")
        if (self.beasts[1].isalive or self.beasts[2].isalive):
            print("Team A: ")
            if (self.beasts[1].isalive):
                print("  Slot 1: " + self.beasts[1].name.ljust(16," ") + str(self.beasts[1].HP).ljust(3," ") + "/" + str(self.beasts[1].maxHP).ljust(3," ") + " HP (" + str(ceil(self.beasts[1].HP/self.beasts[1].maxHP*100)).ljust(3," ") + "%)")
            if (self.beasts[2].isalive):
                print("  Slot 2: " + self.beasts[2].name.ljust(16," ") + str(self.beasts[2].HP).ljust(3," ") + "/" + str(self.beasts[2].maxHP).ljust(3," ") + " HP (" + str(ceil(self.beasts[4].HP/self.beasts[2].maxHP*100)).ljust(3," ") + "%)")
        if (self.beasts[3].isalive or self.beasts[4].isalive):
            print("Team B: ")
            if (self.beasts[3].isalive):
                print("  Slot 3: " + self.beasts[3].name.ljust(16," ") + str(self.beasts[3].HP).ljust(3," ") + "/" + str(self.beasts[3].maxHP).ljust(3," ") + " HP (" + str(ceil(self.beasts[3].HP/self.beasts[3].maxHP*100)).ljust(3," ") + "%)")
            if (self.beasts[4].isalive):
                print("  Slot 4: " + self.beasts[4].name.ljust(16," ") + str(self.beasts[4].HP).ljust(3," ") + "/" + str(self.beasts[4].maxHP).ljust(3," ") + " HP (" + str(ceil(self.beasts[4].HP/self.beasts[4].maxHP*100)).ljust(3," ") + "%)")
        print("###########################################")

    def tick(self):
        #increment turn tracker
        for slot, beast in enumerate(self.beasts[1:],start=1):
            self.turnTracker[slot] = self.turnTracker[slot] + beast.SPE

        #set flags
        for slot, beast in enumerate(self.beasts[1:],start=1):
            if (beast.isalive):
                #check if tt exceeds threshold
                if (beast.selected_attack[0].name != Attack().name): #has any move selected (moving to attack)
                    if (self.turnTracker[slot] >= self.turnTrackerLength/2):
                        self.beasts[slot].setflag(0)
                else: #no move selected (moving from attack)
                    if (self.turnTracker[slot] >= self.turnTrackerLength):
                        self.beasts[slot].setflag(1)
