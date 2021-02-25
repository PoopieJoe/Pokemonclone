class Beast:
    "Describes an ingame beast, complete with stats and equipment"
    def __init__(self, name = "none", species = "none", maxHP = 1, ATK = 0, DEF = 1, heatRES = 0, coldRES = 0, shockRES = 0, SPE = 0):
        #details
        self.species = species
        self.name = name

        #basestats --> move these to a species list
        self.baseMaxHP = maxHP
        self.baseATK = ATK
        self.baseDEF = DEF
        self.baseHeatRES = heatRES
        self.baseColdRES = coldRES
        self.baseShockRES  = shockRES
        self.baseSPE = SPE

        #stats
        self.maxHP = self.baseMaxHP
        self.HP = self.maxHP
        self.ATK = self.baseATK
        self.DEF = self.baseDEF
        self.heatRES = self.baseHeatRES
        self.coldRES = self.baseColdRES
        self.shockRES = self.baseShockRES
        self.SPE = self.baseSPE

        #status
        self.isalive = False
        self.statuseffects = []

        self.attacks = []
        self.selected_attack = [None,0]

        #Equipment
        self.equipmentslots = []
        self.equipment = []

        #Flags
        self.flags = [["execute_attack",False],["choose_attack",False]]

    def selectattack(self,atk_id):
        self.selected_attack[0] = self.attacks[atk_id]
        print(str(self.name) + " selected " + self.selected_attack[0].name)
    
    def selecttarget(self,scene,slot):
        self.selected_attack[1] = slot
        print(str(self.name) + " selected " + str(scene.beasts[slot].name))

    def addstatuseffect(self,name):
        self.statuseffects.append(name)

    def death(self):
        self.HP = 0
        self.SPE = 0
        self.isalive = False

    def setflag(self,flag):
        self.flags[flag][1] = True

    def clearflag(self,flag):
        self.flags[flag][1] = False

    def clearALLflags(self):
        for flag in self.flags:
            flag[1] = False

    def equipItem(self,equipment):
        self.equipment.append(equipment)
        for bonus in equipment.statbonuses:
            if (bonus[0] == "maxHP"):
                self.maxHP += bonus[1]
            elif (bonus[0] == "ATK"):
                self.ATK += bonus[1]
            elif (bonus[0] == "SPE"):
                self.SPE += bonus[1]
            elif (bonus[0] == "DEF"):
                self.DEF += bonus[1]
            elif (bonus[0] == "heatRES"):
                self.heatRES += bonus[1]
            elif (bonus[0] == "coldRES"):
                self.coldRES += bonus[1]
            elif (bonus[0] == "shockRES"):
                self.shockRES += bonus[1]
        
        for attack in equipment.attacks:
            if (attack not in self.attacks):
                self.attacks.append(attack)

class Equipment:
    def __init__(self, name = "none", attacks = [], statbonuses = []):
        self.name = name
        self.attacks = attacks
        self.statbonuses = statbonuses

class Attack:
    def __init__(self, name = "none", power = 0, element = "none", accuracy = 0):
        self.name = name
        self.power = power
        self.element = element
        self.accuracy = accuracy