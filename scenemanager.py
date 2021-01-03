from classes import Beast, Attack
from math import floor

class Scene:
    def __init__(self):
        self.beasts = [Beast(),Beast(),Beast(),Beast(),Beast()]
        self.turnTracker = [0,0,0,0,0]
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
        if (self.beasts[1].isalive == True or self.beasts[2].isalive == True):
            print("Team A: ")
            if (self.beasts[1].isalive == True):
                print("  Slot 1: " + self.beasts[1].name.ljust(16," ") + str(self.beasts[1].HP).ljust(3," ") + "/" + str(self.beasts[1].maxHP).ljust(3," ") + " HP (" + str(floor(self.beasts[1].HP/self.beasts[1].maxHP*100)).ljust(3," ") + "%)")
            if (self.beasts[2].isalive == True):
                print("  Slot 2: " + self.beasts[2].name.ljust(16," ") + str(self.beasts[2].HP).ljust(3," ") + "/" + str(self.beasts[2].maxHP).ljust(3," ") + " HP (" + str(floor(self.beasts[4].HP/self.beasts[2].maxHP*100)).ljust(3," ") + "%)")
        if (self.beasts[3].isalive == True or self.beasts[4].isalive == True):
            print("Team B: ")
            if (self.beasts[3].isalive == True):
                print("  Slot 3: " + self.beasts[3].name.ljust(16," ") + str(self.beasts[3].HP).ljust(3," ") + "/" + str(self.beasts[3].maxHP).ljust(3," ") + " HP (" + str(floor(self.beasts[3].HP/self.beasts[3].maxHP*100)).ljust(3," ") + "%)")
            if (self.beasts[4].isalive == True):
                print("  Slot 4: " + self.beasts[4].name.ljust(16," ") + str(self.beasts[4].HP).ljust(3," ") + "/" + str(self.beasts[4].maxHP).ljust(3," ") + " HP (" + str(floor(self.beasts[4].HP/self.beasts[4].maxHP*100)).ljust(3," ") + "%)")
        print("###########################################")

    def tick(self):
        #increment turn tracker
        for slot in range(1,len(self.beasts)):
            self.turnTracker[slot] = self.turnTracker[slot] + self.beasts[slot].SPE

        #set flags
        for slot, beast in enumerate(self.beasts[1:],start=1):
            if (beast.isalive == True):
                #check if tt exceeds threshold
                if (beast.selected_attack[0].name != Attack().name): #has any move selected (moving to attack)
                    if (self.turnTracker[slot] > 1000):
                        self.beasts[slot].setflag(0)
                else: #no move selected (moving from attack)
                    if (self.turnTracker[slot] > 2000):
                        self.beasts[slot].setflag(1)
